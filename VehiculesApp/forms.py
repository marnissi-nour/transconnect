from django import forms

from EntreprisesApp.models import Entreprise

from .models import Vehicule


class VehiculeForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and user.role != "administrateur":
            self.fields["entreprise"].queryset = (
                Entreprise.objects.filter(gerant=user)
                if getattr(user, "entreprise", None)
                else self.fields["entreprise"].queryset.none()
            )

    class Meta:
        model = Vehicule
        fields = ['immatriculation', 'type_vehicule', 'capacite_kg', 'disponible', 'entreprise']
        widgets = {
            'immatriculation': forms.TextInput(attrs={'class': 'form-control'}),
            'type_vehicule': forms.Select(attrs={'class': 'form-control'}),
            'capacite_kg': forms.NumberInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'entreprise': forms.Select(attrs={'class': 'form-control'}),

        }
