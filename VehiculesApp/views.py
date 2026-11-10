from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from VehiculesApp.forms import VehiculeForm

from .models import Vehicule


class VehiculeListView(ListView):
    model = Vehicule
    template_name = "vehicules/liste.html"
    context_object_name = "vehicules"

    def get_queryset(self):
        queryset = Vehicule.objects.select_related("entreprise")
        search = self.request.GET.get("q", "").strip()
        type_vehicule = self.request.GET.get("type_vehicule", "").strip()
        disponible = self.request.GET.get("disponible", "").strip()
        entreprise = self.request.GET.get("entreprise", "").strip()

        if search:
            queryset = queryset.filter(
                Q(immatriculation__icontains=search)
                | Q(type_vehicule__icontains=search)
                | Q(entreprise__raison_social__icontains=search)
            )
        if type_vehicule:
            queryset = queryset.filter(type_vehicule=type_vehicule)
        if disponible in {"true", "false"}:
            queryset = queryset.filter(disponible=disponible == "true")
        if entreprise:
            queryset = queryset.filter(
                entreprise__raison_social__icontains=entreprise
            )

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = {
            key: self.request.GET.get(key, "")
            for key in ("q", "type_vehicule", "disponible", "entreprise")
        }
        context["type_choices"] = Vehicule._meta.get_field(
            "type_vehicule"
        ).choices
        return context


class VehiculeCreateView(CreateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = "vehicules/form.html"
    #fields = '__all__'
    success_url = reverse_lazy("vehicules:liste")

class VehiculeUpdateView(UpdateView):
    model = Vehicule
    form_class = VehiculeForm
    template_name = "vehicules/form.html"
    success_url = reverse_lazy("vehicules:liste")

    def get_object(self, queryset=None):
        return get_object_or_404(Vehicule, pk=self.kwargs.get("pk"))

def detail_vehicule(request, pk):
    vehicule = get_object_or_404(
        Vehicule.objects.select_related("entreprise"), pk=pk
    )
    return render(request, "vehicules/detail.html", {"vehicule": vehicule})


class VehiculeDeleteView(DeleteView):
    model = Vehicule
    template_name = "vehicules/confirmer_suppression.html"
    context_object_name = "objet"
    success_url = reverse_lazy("vehicules:liste")
