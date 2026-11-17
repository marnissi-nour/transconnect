from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from config.access import RoleRequiredMixin, is_admin, user_entreprise

from VehiculesApp.forms import VehiculeForm

from .models import Vehicule


class VehiculeListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    allowed_roles = ("transporteur", "administrateur")
    model = Vehicule
    template_name = "vehicules/liste.html"
    context_object_name = "vehicules"
    paginate_by = 10

    def get_queryset(self):
        queryset = Vehicule.objects.select_related("entreprise")
        if not is_admin(self.request.user):
            entreprise = user_entreprise(self.request.user)
            queryset = (
                queryset.filter(entreprise=entreprise)
                if entreprise and self.request.user.role == "transporteur"
                else queryset.none()
            )
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


class VehiculeCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ("transporteur", "administrateur")
    model = Vehicule
    form_class = VehiculeForm
    template_name = "vehicules/form.html"
    #fields = '__all__'
    success_url = reverse_lazy("vehicules:liste")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class VehiculeUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ("transporteur", "administrateur")
    model = Vehicule
    form_class = VehiculeForm
    template_name = "vehicules/form.html"
    success_url = reverse_lazy("vehicules:liste")

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.kwargs.get("pk"))

    def get_queryset(self):
        queryset = Vehicule.objects.all()
        if is_admin(self.request.user):
            return queryset
        entreprise = user_entreprise(self.request.user)
        return queryset.filter(entreprise=entreprise) if entreprise else queryset.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


@login_required
def detail_vehicule(request, pk):
    queryset = Vehicule.objects.select_related("entreprise")
    if not is_admin(request.user):
        entreprise = user_entreprise(request.user)
        queryset = queryset.filter(entreprise=entreprise) if (
            entreprise and request.user.role == "transporteur"
        ) else queryset.none()
    vehicule = get_object_or_404(queryset, pk=pk)
    return render(request, "vehicules/detail.html", {"vehicule": vehicule})


class VehiculeDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    allowed_roles = ("transporteur", "administrateur")
    model = Vehicule
    template_name = "vehicules/confirmer_suppression.html"
    context_object_name = "objet"
    success_url = reverse_lazy("vehicules:liste")

    def get_queryset(self):
        queryset = super().get_queryset()
        if is_admin(self.request.user):
            return queryset
        entreprise = user_entreprise(self.request.user)
        return queryset.filter(entreprise=entreprise) if entreprise else queryset.none()
