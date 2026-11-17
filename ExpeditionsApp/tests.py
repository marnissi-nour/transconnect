from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from EntreprisesApp.models import Entreprise, Utilisateur
from OffersApp.models import Offre
from VehiculesApp.models import Vehicule
from NotificationsApp.models import Notification

from .models import Expedition, ExpeditionEvenement


class ExpeditionHistoryTests(TestCase):
    def setUp(self):
        self.chargeur = Utilisateur.objects.create_user(
            username="chargeur",
            email="chargeur@gmail.com",
            password="password123",
            telephone="12345678",
            role="chargeur",
        )
        self.transporteur = Utilisateur.objects.create_user(
            username="transporteur",
            email="transporteur@gmail.com",
            password="password123",
            telephone="87654321",
            role="transporteur",
        )
        self.entreprise_chargeur = Entreprise.objects.create(
            raison_social="Chargeur Test",
            matricule_fiscal="1234567/A/B/M/001",
            type_entreprise="chargeur",
            adresse="12 rue de test suffisamment longue",
            gerant=self.chargeur,
        )
        self.entreprise_transporteur = Entreprise.objects.create(
            raison_social="Transporteur Test",
            matricule_fiscal="1234567/A/B/M/002",
            type_entreprise="transporteur",
            adresse="14 rue de test suffisamment longue",
            gerant=self.transporteur,
        )

    def test_status_changes_are_recorded(self):
        expedition = Expedition.objects.create(
            ville_depart="Tunis",
            ville_arrive="Sousse",
            date_souhaitee=date.today() + timedelta(days=2),
            poids_kg=Decimal("1000.00"),
            description="Marchandise de test",
            entreprise=self.entreprise_chargeur,
        )

        expedition.statut = "en_cours"
        expedition._status_changed_by = self.chargeur
        expedition.save()

        historique = expedition.historique_statuts.order_by("changed_at")
        self.assertEqual(historique.count(), 2)
        self.assertEqual(historique.last().ancien_statut, "publiee")
        self.assertEqual(historique.last().nouveau_statut, "en_cours")

    def test_new_offer_creates_chargeur_notification(self):
        expedition = Expedition.objects.create(
            ville_depart="Tunis",
            ville_arrive="Sousse",
            date_souhaitee=date.today() + timedelta(days=2),
            poids_kg=Decimal("1000.00"),
            description="Marchandise de test",
            entreprise=self.entreprise_chargeur,
        )
        vehicule = Vehicule.objects.create(
            immatriculation="123-TUN-01",
            type_vehicule="camionnette",
            capacite_kg=1500,
            entreprise=self.entreprise_transporteur,
        )

        Offre.objects.create(
            prix=Decimal("250.00"),
            delai_jours=2,
            transporteur=self.entreprise_transporteur,
            expedition=expedition,
            vehicule=vehicule,
        )

        notification = Notification.objects.get(
            destinataire=self.chargeur,
            offre__expedition=expedition,
        )
        self.assertFalse(notification.lue)

    def test_delivery_event_keeps_timestamp_and_author(self):
        expedition = Expedition.objects.create(
            ville_depart="Tunis",
            ville_arrive="Sousse",
            date_souhaitee=date.today() + timedelta(days=2),
            poids_kg=Decimal("1000.00"),
            description="Marchandise de test",
            entreprise=self.entreprise_chargeur,
        )
        occurred_at = timezone.now() - timedelta(hours=1)

        evenement = ExpeditionEvenement.objects.create(
            expedition=expedition,
            type_evenement="depart",
            description="Le véhicule a quitté le dépôt.",
            occurred_at=occurred_at,
            created_by=self.transporteur,
        )

        self.assertEqual(evenement.occurred_at, occurred_at)
        self.assertEqual(evenement.created_by, self.transporteur)
