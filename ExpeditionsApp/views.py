from django.db.models import Q
from decimal import Decimal, InvalidOperation

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from config.access import RoleRequiredMixin, is_admin, user_entreprise

from .models import Expedition
from .forms import ExpeditionEvenementForm, ExpeditionForm


class ExpeditionListView(LoginRequiredMixin, ListView):
    model = Expedition
    template_name = "expeditions/liste.html"
    context_object_name = "expeditions"
    paginate_by = 10

    def get_queryset(self):
        queryset = Expedition.objects.select_related("entreprise")
        if not is_admin(self.request.user):
            entreprise = user_entreprise(self.request.user)
            if self.request.user.role == "chargeur":
                queryset = queryset.filter(entreprise=entreprise) if entreprise else queryset.none()
            else:
                queryset = queryset.filter(
                    Q(statut="publiee") | Q(offres__transporteur=entreprise)
                ).distinct() if entreprise else queryset.none()
        search = self.request.GET.get("q", "").strip()
        statut = self.request.GET.get("statut", "").strip()
        depart = self.request.GET.get("depart", "").strip()
        arrivee = self.request.GET.get("arrivee", "").strip()

        if search:
            queryset = queryset.filter(
                Q(reference__icontains=search)
                | Q(ville_depart__icontains=search)
                | Q(ville_arrive__icontains=search)
                | Q(description__icontains=search)
            )
        if statut:
            queryset = queryset.filter(statut=statut)
        if depart:
            queryset = queryset.filter(ville_depart__icontains=depart)
        if arrivee:
            queryset = queryset.filter(ville_arrive__icontains=arrivee)
        poids_min = self.request.GET.get("poids_min", "").strip()
        poids_max = self.request.GET.get("poids_max", "").strip()
        try:
            if poids_min:
                queryset = queryset.filter(poids_kg__gte=Decimal(poids_min))
        except InvalidOperation:
            pass
        try:
            if poids_max:
                queryset = queryset.filter(poids_kg__lte=Decimal(poids_max))
        except InvalidOperation:
            pass

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            "q": self.request.GET.get("q", ""),
            "statut": self.request.GET.get("statut", ""),
            "depart": self.request.GET.get("depart", ""),
            "arrivee": self.request.GET.get("arrivee", ""),
            "poids_min": self.request.GET.get("poids_min", ""),
            "poids_max": self.request.GET.get("poids_max", ""),
        }
        context["statut_choices"] = Expedition._meta.get_field(
            "statut"
        ).choices
        return context


class ExpeditionCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ("chargeur", "administrateur")
    model = Expedition
    form_class = ExpeditionForm
    template_name = "expeditions/form.html"
    success_url = reverse_lazy("expeditions:liste")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance._status_changed_by = self.request.user
        return super().form_valid(form)


class ExpeditionUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ("chargeur", "administrateur")
    model = Expedition
    form_class = ExpeditionForm
    template_name = "expeditions/form.html"
    slug_field = "reference"
    slug_url_kwarg = "reference"
    success_url = reverse_lazy("expeditions:liste")

    def get_queryset(self):
        queryset = super().get_queryset()
        if is_admin(self.request.user):
            return queryset
        entreprise = user_entreprise(self.request.user)
        return queryset.filter(entreprise=entreprise) if entreprise else queryset.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance._status_changed_by = self.request.user
        return super().form_valid(form)


"""
Previous function-based implementation:

def detail_expedition(request, reference):
    expedition = get_object_or_404(
        Expedition.objects.select_related("entreprise"),
        reference=reference,
    )
    offres = expedition.offres.select_related(
        "transporteur",
        "vehicule",
    ).order_by("-date_proposition")
    return render(
        request,
        "expeditions/detail.html",
        {"expedition": expedition, "offres": offres},
    )
"""


class ExpeditionDetailView(LoginRequiredMixin, DetailView):
    model = Expedition
    template_name = "expeditions/detail.html"
    context_object_name = "expedition"
    slug_field = "reference"
    slug_url_kwarg = "reference"

    def get_queryset(self):
        queryset = Expedition.objects.select_related("entreprise")
        if is_admin(self.request.user):
            return queryset
        entreprise = user_entreprise(self.request.user)
        if self.request.user.role == "chargeur":
            return queryset.filter(entreprise=entreprise) if entreprise else queryset.none()
        return queryset.filter(
            Q(statut="publiee") | Q(offres__transporteur=entreprise)
        ).distinct() if entreprise else queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["offres"] = self.object.offres.select_related(
            "transporteur",
            "vehicule",
        ).order_by("-date_proposition")
        context["evenements"] = self.object.evenements_suivi.select_related(
            "created_by"
        )
        context["evenement_form"] = ExpeditionEvenementForm()
        return context


@login_required
def ajouter_evenement(request, reference):
    queryset = Expedition.objects.all()
    if not is_admin(request.user):
        entreprise = user_entreprise(request.user)
        if request.user.role == "chargeur":
            queryset = queryset.filter(entreprise=entreprise)
        elif request.user.role == "transporteur":
            queryset = queryset.filter(
                offres__transporteur=entreprise
            )
        else:
            queryset = queryset.none()

    expedition = get_object_or_404(queryset, reference=reference)
    if request.method == "POST":
        form = ExpeditionEvenementForm(request.POST)
        if form.is_valid():
            evenement = form.save(commit=False)
            evenement.expedition = expedition
            evenement.created_by = request.user
            evenement.save()
            return redirect("expeditions:detail", reference=reference)
    else:
        form = ExpeditionEvenementForm()
    return render(
        request,
        "expeditions/evenement_form.html",
        {"expedition": expedition, "form": form},
    )


class ExpeditionDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    allowed_roles = ("chargeur", "administrateur")
    model = Expedition
    template_name = "expeditions/confirmer_suppression.html"
    context_object_name = "objet"
    slug_field = "reference"
    slug_url_kwarg = "reference"
    success_url = reverse_lazy("expeditions:liste")

    def get_queryset(self):
        queryset = super().get_queryset()
        if is_admin(self.request.user):
            return queryset
        entreprise = user_entreprise(self.request.user)
        return queryset.filter(entreprise=entreprise) if entreprise else queryset.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_objet"] = "l'expédition"
        return context
