from django import forms

from .models import Offre


class OffreForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and user.role != "administrateur":
            entreprise = getattr(user, "entreprise", None)
            if entreprise is None:
                self.fields["transporteur"].queryset = (
                    self.fields["transporteur"].queryset.none()
                )
                self.fields["vehicule"].queryset = (
                    self.fields["vehicule"].queryset.none()
                )
                self.fields["expedition"].queryset = (
                    self.fields["expedition"].queryset.none()
                )
            else:
                self.fields["transporteur"].queryset = (
                    self.fields["transporteur"].queryset.filter(pk=entreprise.pk)
                )
                self.fields["vehicule"].queryset = entreprise.vehicules.all()
                self.fields["expedition"].queryset = (
                    self.fields["expedition"].queryset.filter(statut="publiee")
                )

    class Meta:
        model = Offre
        fields = [
            "prix",
            "delai_jours",
            "statut",
            "transporteur",
            "expedition",
            "vehicule",
        ]
