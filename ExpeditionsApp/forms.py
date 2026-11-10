from django import forms

from .models import Expedition


class ExpeditionForm(forms.ModelForm):
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
