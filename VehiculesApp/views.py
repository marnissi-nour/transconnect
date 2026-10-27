from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Vehicule


def liste_vehicules(request):
    vehicules = Vehicule.objects.select_related("entreprise").order_by(
        "-created_at"
    )
    return render(request, "vehicules/liste.html", {"vehicules": vehicules})


def detail_vehicule(request, pk):
    vehicule = get_object_or_404(
        Vehicule.objects.select_related("entreprise"), pk=pk
    )
    return render(request, "vehicules/detail.html", {"vehicule": vehicule})


@require_http_methods(["GET", "POST"])
def supprimer_vehicule(request, pk):
    vehicule = get_object_or_404(Vehicule, pk=pk)
    if request.method == "POST":
        vehicule.delete()
        return HttpResponseRedirect(reverse("vehicules:liste"))
    return render(
        request,
        "vehicules/confirmer_suppression.html",
        {"objet": vehicule},
    )
