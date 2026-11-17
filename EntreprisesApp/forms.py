from django import forms

from .models import Entreprise


class EntrepriseForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and user.role != "administrateur":
            self.fields["gerant"].queryset = user.__class__.objects.filter(
                pk=user.pk
            )
            self.fields["type_entreprise"].choices = [
                choice
                for choice in self.fields["type_entreprise"].choices
                if choice[0] == user.role
            ]

    class Meta:
        model = Entreprise
        fields = [
            "raison_social",
            "matricule_fiscal",
            "type_entreprise",
            "adresse",
            "gerant",
        ]
