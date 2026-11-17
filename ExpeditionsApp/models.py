from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Expedition(models.Model):
    reference = models.CharField(
        max_length=12,
        unique=True,
        editable=False
    )

    ville_depart = models.CharField(max_length=100)
    ville_arrive = models.CharField(max_length=100)

    date_souhaitee = models.DateField()

    poids_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    description = models.TextField()

    statut = models.CharField(
        max_length=20,
        choices=[
            ("publiee", "Publiée"),
            ("attribuee", "Attribuée"),
            ("en_cours", "En cours"),
            ("livree", "Livrée"),
            ("annulee", "Annulée"),
        ],
        default="publiee"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entreprise = models.ForeignKey(
        "EntreprisesApp.Entreprise",
        on_delete=models.CASCADE,
        related_name="expeditions"
    )

    def save(self, *args, **kwargs):
        ancien_statut = None
        if self.pk:
            ancien_statut = (
                Expedition.objects.filter(pk=self.pk)
                .values_list("statut", flat=True)
                .first()
            )

        if not self.reference:
            from django.utils import timezone

            prefix = f"EXP-{timezone.now().year % 100:02d}-"

            references = Expedition.objects.filter(
                reference__startswith=prefix
            ).values_list("reference", flat=True)

            numeros = [
                int(ref[-5:])
                for ref in references
                if ref[-5:].isdigit()
            ]

            prochain = max(numeros, default=0) + 1

            if prochain > 99999:
                raise ValidationError(
                    "Le compteur des expéditions est épuisé pour cette année."
                )

            self.reference = f"{prefix}{prochain:05d}"


        self.full_clean()
        super().save(*args, **kwargs)

        if ancien_statut != self.statut:
            ExpeditionStatutHistorique.objects.create(
                expedition=self,
                ancien_statut=ancien_statut,
                nouveau_statut=self.statut,
                changed_by=getattr(self, "_status_changed_by", None),
            )

    def clean(self):
        super().clean()

        if self.entreprise_id:
            if self.entreprise.type_entreprise != "chargeur":
                raise ValidationError({
                    "entreprise": (
                        "Une expédition doit appartenir à une "
                        "entreprise de type chargeur."
                    )
                })

    def __str__(self):
        return (
            f"{self.reference} - "
            f"{self.ville_depart} → {self.ville_arrive}"
        )


class ExpeditionStatutHistorique(models.Model):
    expedition = models.ForeignKey(
        Expedition,
        on_delete=models.CASCADE,
        related_name="historique_statuts",
    )
    ancien_statut = models.CharField(max_length=20, blank=True, null=True)
    nouveau_statut = models.CharField(max_length=20)
    changed_by = models.ForeignKey(
        "EntreprisesApp.Utilisateur",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="changements_statut_expedition",
    )
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-changed_at",)

    def __str__(self):
        return (
            f"{self.expedition.reference}: "
            f"{self.ancien_statut or '—'} → {self.nouveau_statut}"
        )

    @property
    def ancien_statut_libelle(self):
        return dict(Expedition._meta.get_field("statut").choices).get(
            self.ancien_statut,
            "Création",
        )

    @property
    def nouveau_statut_libelle(self):
        return dict(Expedition._meta.get_field("statut").choices).get(
            self.nouveau_statut,
            self.nouveau_statut,
        )


class ExpeditionEvenement(models.Model):
    TYPE_CHOICES = [
        ("collecte", "Collecte"),
        ("depart", "Départ"),
        ("transit", "En transit"),
        ("livraison", "Livraison"),
        ("incident", "Incident"),
    ]

    expedition = models.ForeignKey(
        Expedition,
        on_delete=models.CASCADE,
        related_name="evenements_suivi",
    )
    type_evenement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    occurred_at = models.DateTimeField()
    created_by = models.ForeignKey(
        "EntreprisesApp.Utilisateur",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="evenements_suivi_crees",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-occurred_at", "-created_at")

