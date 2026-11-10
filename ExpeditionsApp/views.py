from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Expedition
from .forms import ExpeditionForm


class ExpeditionListView(ListView):
    model = Expedition
    template_name = "expeditions/liste.html"
    context_object_name = "expeditions"

    def get_queryset(self):
        queryset = Expedition.objects.select_related("entreprise")
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

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            "q": self.request.GET.get("q", ""),
            "statut": self.request.GET.get("statut", ""),
            "depart": self.request.GET.get("depart", ""),
            "arrivee": self.request.GET.get("arrivee", ""),
        }
        context["statut_choices"] = Expedition._meta.get_field(
            "statut"
        ).choices
        return context


class ExpeditionCreateView(CreateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = "expeditions/form.html"
    success_url = reverse_lazy("expeditions:liste")


class ExpeditionUpdateView(UpdateView):
    model = Expedition
    form_class = ExpeditionForm
    template_name = "expeditions/form.html"
    slug_field = "reference"
    slug_url_kwarg = "reference"
    success_url = reverse_lazy("expeditions:liste")


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


class ExpeditionDetailView(DetailView):
    model = Expedition
    template_name = "expeditions/detail.html"
    context_object_name = "expedition"
    slug_field = "reference"
    slug_url_kwarg = "reference"

    def get_queryset(self):
        return Expedition.objects.select_related("entreprise")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["offres"] = self.object.offres.select_related(
            "transporteur",
            "vehicule",
        ).order_by("-date_proposition")
        return context


class ExpeditionDeleteView(DeleteView):
    model = Expedition
    template_name = "expeditions/confirmer_suppression.html"
    context_object_name = "objet"
    slug_field = "reference"
    slug_url_kwarg = "reference"
    success_url = reverse_lazy("expeditions:liste")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_objet"] = "l'expédition"
        return context
