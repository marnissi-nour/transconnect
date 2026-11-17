from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from config.access import RoleRequiredMixin, is_admin, user_entreprise

from .models import Offre
from .forms import OffreForm


class OffreListView(LoginRequiredMixin, ListView):
    model = Offre
    template_name = "offres/liste.html"
    context_object_name = "offres"

    def get_queryset(self):
        queryset = Offre.objects.select_related(
            "transporteur", "expedition", "vehicule"
        )
        if not is_admin(self.request.user):
            entreprise = user_entreprise(self.request.user)
            if self.request.user.role == "transporteur":
                queryset = (
                    queryset.filter(transporteur=entreprise)
                    if entreprise else queryset.none()
                )
            elif self.request.user.role == "chargeur":
                queryset = (
                    queryset.filter(expedition__entreprise=entreprise)
                    if entreprise else queryset.none()
                )
            else:
                queryset = queryset.none()
        search = self.request.GET.get("q", "").strip()
        statut = self.request.GET.get("statut", "").strip()
        transporteur = self.request.GET.get("transporteur", "").strip()

        if search:
            queryset = queryset.filter(
                Q(transporteur__raison_social__icontains=search)
                | Q(expedition__reference__icontains=search)
                | Q(vehicule__immatriculation__icontains=search)
            )
        if statut:
            queryset = queryset.filter(statut=statut)
        if transporteur:
            queryset = queryset.filter(
                transporteur__raison_social__icontains=transporteur
            )

        return queryset.order_by("-date_proposition")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            key: self.request.GET.get(key, "")
            for key in ("q", "statut", "transporteur")
        }
        context["statut_choices"] = Offre._meta.get_field(
            "statut"
        ).choices
        return context


class OffreCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ("transporteur", "administrateur")
    model = Offre
    form_class = OffreForm
    template_name = "offres/form.html"
    success_url = reverse_lazy("offres:liste")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class OffreUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ("transporteur", "administrateur")
    model = Offre
    form_class = OffreForm
    template_name = "offres/form.html"
    success_url = reverse_lazy("offres:liste")

    def get_queryset(self):
        queryset = super().get_queryset()
        if is_admin(self.request.user):
            return queryset
        entreprise = user_entreprise(self.request.user)
        return queryset.filter(transporteur=entreprise) if entreprise else queryset.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


@login_required
def detail_offre(request, pk):
    queryset = Offre.objects.select_related(
        "transporteur", "expedition", "vehicule"
    )
    if not is_admin(request.user):
        entreprise = user_entreprise(request.user)
        if request.user.role == "transporteur":
            queryset = queryset.filter(transporteur=entreprise) if entreprise else queryset.none()
        else:
            queryset = queryset.filter(expedition__entreprise=entreprise) if entreprise else queryset.none()
    offre = get_object_or_404(queryset, pk=pk)
    return render(request, "offres/detail.html", {"offre": offre})


class OffreDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    allowed_roles = ("transporteur", "administrateur")
    model = Offre
    template_name = "offres/confirmer_suppression.html"
    context_object_name = "objet"
    success_url = reverse_lazy("offres:liste")

    def get_queryset(self):
        queryset = super().get_queryset()
        if is_admin(self.request.user):
            return queryset
        entreprise = user_entreprise(self.request.user)
        return queryset.filter(transporteur=entreprise) if entreprise else queryset.none()
