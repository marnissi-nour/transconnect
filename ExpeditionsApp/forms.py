from django import forms
from django.utils import timezone

from EntreprisesApp.models import Entreprise

from .models import Expedition, ExpeditionEvenement


class ExpeditionForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and user.role != "administrateur":
            self.fields["entreprise"].queryset = (
                Entreprise.objects.filter(gerant=user)
                if getattr(user, "entreprise", None)
                else self.fields["entreprise"].queryset.none()
            )

    class Meta:
        model = Expedition
        fields = [
            "ville_depart",
            "ville_arrive",
            "date_souhaitee",
            "poids_kg",
            "description",
            "statut",
            "entreprise",
        ]


class ExpeditionEvenementForm(forms.ModelForm):
    class Meta:
        model = ExpeditionEvenement
        fields = ["type_evenement", "description", "occurred_at"]
        widgets = {
            "occurred_at": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["occurred_at"].initial = timezone.localtime().strftime(
            "%Y-%m-%dT%H:%M"
        )
