from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Entreprise


def liste_entreprises(request):
    entreprises = Entreprise.objects.select_related("gerant").order_by(
        "raison_social"
    )
    return render(
        request,
        "entreprises/liste.html",
        {"entreprises": entreprises},
    )


def detail_entreprise(request, pk):
    entreprise = get_object_or_404(
        Entreprise.objects.select_related("gerant"), pk=pk
    )
    return render(
        request,
        "entreprises/detail.html",
        {"entreprise": entreprise},
    )


@require_http_methods(["GET", "POST"])
def supprimer_entreprise(request, pk):
    entreprise = get_object_or_404(Entreprise, pk=pk)
    if request.method == "POST":
        entreprise.delete()
        return HttpResponseRedirect(reverse("entreprises:liste"))
    return render(
        request,
        "entreprises/confirmer_suppression.html",
        {"objet": entreprise},
    )
