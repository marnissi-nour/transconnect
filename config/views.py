from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from EntreprisesApp.models import Entreprise, Utilisateur
from ExpeditionsApp.models import Expedition
from OffersApp.models import Offre
from VehiculesApp.models import Vehicule

from .forms import (
    ProfileForm,
    SignUpForm,
    TransConnectAuthenticationForm,
)


def home(request):
    return render(request, "home.html")


class TransConnectLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = TransConnectAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard")


class TransConnectLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user


class TransConnectPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("password_change_done")


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


@login_required
def dashboard(request):
    role = request.user.role
    entreprise = getattr(request.user, "entreprise", None)
    stats = []
    recent_items = []

    if role == "administrateur":
        stats = [
            ("Utilisateurs", Utilisateur.objects.count(), "Tous les comptes"),
            ("Entreprises", Entreprise.objects.count(), "Partenaires inscrits"),
            ("Véhicules", Vehicule.objects.count(), "Flotte enregistrée"),
            ("Expéditions", Expedition.objects.count(), "Dossiers suivis"),
        ]
        recent_items = (
            Expedition.objects.select_related("entreprise")
            .order_by("-created_at")[:5]
        )
    else:
        if entreprise is None:
            stats = [
                ("Profil", 1, "Compte actif"),
                ("Entreprise", 0, "À compléter"),
            ]
        elif role == "chargeur":
            stats = [
                ("Expéditions", entreprise.expeditions.count(), "Créées par votre entreprise"),
                (
                    "Offres reçues",
                    Offre.objects.filter(
                        expedition__entreprise=entreprise
                    ).count(),
                    "Propositions à examiner",
                ),
                ("Statut", 1, entreprise.get_type_entreprise_display()),
            ]
            recent_items = entreprise.expeditions.order_by("-created_at")[:5]
        else:
            stats = [
                ("Véhicules", entreprise.vehicules.count(), "Dans votre flotte"),
                ("Offres envoyées", entreprise.offres.count(), "Propositions déposées"),
                ("Disponibles", entreprise.vehicules.filter(disponible=True).count(), "Véhicules prêts"),
            ]
            recent_items = entreprise.offres.select_related(
                "expedition", "vehicule"
            ).order_by("-created_at")[:5]

    return render(
        request,
        "dashboard.html",
        {
            "stats": stats,
            "recent_items": recent_items,
            "entreprise": entreprise,
            "role": role,
            "role_label": request.user.get_role_display(),
        },
    )


def index(request, nom):
    return render(request, "home.html", {"name": nom})
