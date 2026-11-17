from django import forms

from EntreprisesApp.models import Entreprise

from .models import Expedition


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
