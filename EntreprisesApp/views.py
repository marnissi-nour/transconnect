from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from config.access import RoleRequiredMixin, is_admin, user_entreprise

from .models import Entreprise
from .forms import EntrepriseForm


class EntrepriseListView(LoginRequiredMixin, ListView):
    model = Entreprise
    template_name = "entreprises/liste.html"
    context_object_name = "entreprises"

    def get_queryset(self):
        queryset = Entreprise.objects.select_related("gerant")
        if not is_admin(self.request.user):
            queryset = queryset.filter(gerant=self.request.user)
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


class EntrepriseCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ("chargeur", "transporteur", "administrateur")
    model = Entreprise
    form_class = EntrepriseForm
    template_name = "entreprises/form.html"
    success_url = reverse_lazy("entreprises:liste")

    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user) and user_entreprise(request.user):
            return redirect("entreprises:liste")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not is_admin(self.request.user):
            form.instance.gerant = self.request.user
        return super().form_valid(form)


class EntrepriseUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ("chargeur", "transporteur", "administrateur")
    model = Entreprise
    form_class = EntrepriseForm
    template_name = "entreprises/form.html"
    success_url = reverse_lazy("entreprises:liste")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset if is_admin(self.request.user) else queryset.filter(
            gerant=self.request.user
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not is_admin(self.request.user):
            form.instance.gerant = self.request.user
        return super().form_valid(form)


@login_required
def detail_entreprise(request, pk):
    queryset = Entreprise.objects.select_related("gerant")
    if not is_admin(request.user):
        queryset = queryset.filter(gerant=request.user)
    entreprise = get_object_or_404(queryset, pk=pk)
    return render(
        request,
        "entreprises/detail.html",
        {"entreprise": entreprise},
    )


class EntrepriseDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    allowed_roles = ("chargeur", "transporteur", "administrateur")
    model = Entreprise
    template_name = "entreprises/confirmer_suppression.html"
    context_object_name = "objet"
    success_url = reverse_lazy("entreprises:liste")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset if is_admin(self.request.user) else queryset.filter(
            gerant=self.request.user
        )
