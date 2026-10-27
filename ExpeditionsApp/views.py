from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Expedition


def liste_expeditions(request):
    expeditions = (
        Expedition.objects.filter(statut="publiee")
        .select_related("entreprise")
        .order_by("-created_at")
    )
    return render(
        request,
        "expeditions/liste.html",
        {"expeditions": expeditions},
    )


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


@require_http_methods(["GET", "POST"])
def supprimer_expedition(request, reference):
    expedition = get_object_or_404(Expedition, reference=reference)
    if request.method == "POST":
        expedition.delete()
        return HttpResponseRedirect(reverse("expeditions:liste"))
    return render(
        request,
        "expeditions/confirmer_suppression.html",
        {"objet": expedition, "type_objet": "l'expédition"},
    )
