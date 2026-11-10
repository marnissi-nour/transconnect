from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Entreprise
from .forms import EntrepriseForm


class EntrepriseListView(ListView):
    model = Entreprise
    template_name = "entreprises/liste.html"
    context_object_name = "entreprises"

    def get_queryset(self):
        queryset = Entreprise.objects.select_related("gerant")
        search = self.request.GET.get("q", "").strip()
        type_entreprise = self.request.GET.get("type_entreprise", "").strip()

        if search:
            queryset = queryset.filter(
                Q(raison_social__icontains=search)
                | Q(matricule_fiscal__icontains=search)
                | Q(adresse__icontains=search)
                | Q(gerant__username__icontains=search)
            )
        if type_entreprise:
            queryset = queryset.filter(type_entreprise=type_entreprise)

        return queryset.order_by("raison_social")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            key: self.request.GET.get(key, "")
            for key in ("q", "type_entreprise")
        }
        context["type_choices"] = Entreprise._meta.get_field(
            "type_entreprise"
        ).choices
        return context


class EntrepriseCreateView(CreateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = "entreprises/form.html"
    success_url = reverse_lazy("entreprises:liste")


class EntrepriseUpdateView(UpdateView):
    model = Entreprise
    form_class = EntrepriseForm
    template_name = "entreprises/form.html"
    success_url = reverse_lazy("entreprises:liste")


def detail_entreprise(request, pk):
    entreprise = get_object_or_404(
        Entreprise.objects.select_related("gerant"), pk=pk
    )
    return render(
        request,
        "entreprises/detail.html",
        {"entreprise": entreprise},
    )


class EntrepriseDeleteView(DeleteView):
    model = Entreprise
    template_name = "entreprises/confirmer_suppression.html"
    context_object_name = "objet"
    success_url = reverse_lazy("entreprises:liste")
