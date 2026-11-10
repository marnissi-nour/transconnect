from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Offre
from .forms import OffreForm


class OffreListView(ListView):
    model = Offre
    template_name = "offres/liste.html"
    context_object_name = "offres"

    def get_queryset(self):
        queryset = Offre.objects.select_related(
            "transporteur", "expedition", "vehicule"
        )
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


class OffreCreateView(CreateView):
    model = Offre
    form_class = OffreForm
    template_name = "offres/form.html"
    success_url = reverse_lazy("offres:liste")


class OffreUpdateView(UpdateView):
    model = Offre
    form_class = OffreForm
    template_name = "offres/form.html"
    success_url = reverse_lazy("offres:liste")


def detail_offre(request, pk):
    offre = get_object_or_404(
        Offre.objects.select_related(
            "transporteur", "expedition", "vehicule"
        ),
        pk=pk,
    )
    return render(request, "offres/detail.html", {"offre": offre})


class OffreDeleteView(DeleteView):
    model = Offre
    template_name = "offres/confirmer_suppression.html"
    context_object_name = "objet"
    success_url = reverse_lazy("offres:liste")
