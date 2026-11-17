from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from EntreprisesApp.models import Utilisateur


class TransConnectAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={
                "autocomplete": "username",
                "placeholder": "Votre nom d'utilisateur",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Votre mot de passe",
            }
        ),
    )


class SignUpForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "telephone",
            "role",
        )
        labels = {
            "username": "Nom d'utilisateur",
            "first_name": "Prénom",
            "last_name": "Nom",
            "email": "Adresse Gmail",
            "telephone": "Téléphone",
            "role": "Profil",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={"autocomplete": "username"}
            ),
            "first_name": forms.TextInput(
                attrs={"autocomplete": "given-name"}
            ),
            "last_name": forms.TextInput(
                attrs={"autocomplete": "family-name"}
            ),
            "email": forms.EmailInput(
                attrs={"autocomplete": "email"}
            ),
            "telephone": forms.TextInput(
                attrs={
                    "autocomplete": "tel",
                    "inputmode": "numeric",
                    "maxlength": 8,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = [
            choice for choice in self.fields["role"].choices
            if choice[0] != "administrateur"
        ]
        self.fields["password1"].label = "Mot de passe"
        self.fields["password2"].label = "Confirmation du mot de passe"
        self.fields["password1"].widget.attrs["autocomplete"] = "new-password"
        self.fields["password2"].widget.attrs["autocomplete"] = "new-password"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ("first_name", "last_name", "email", "telephone")
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "email": "Adresse Gmail",
            "telephone": "Téléphone",
        }
        widgets = {
            "first_name": forms.TextInput(
                attrs={"autocomplete": "given-name"}
            ),
            "last_name": forms.TextInput(
                attrs={"autocomplete": "family-name"}
            ),
            "email": forms.EmailInput(
                attrs={"autocomplete": "email"}
            ),
            "telephone": forms.TextInput(
                attrs={"autocomplete": "tel", "inputmode": "numeric"}
            ),
        }
