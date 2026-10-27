from django.shortcuts import get_object_or_404, render

from .models import Expedition


def list_expeditions(request):
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


def expedition_detail(request, reference):
    expedition = get_object_or_404(
        Expedition.objects.select_related("entreprise"),
        reference=reference,
    )
    offres = expedition.offres.select_related(
        "transporteur",
        "vehicule",
    ).order_by("-created_at")
    return render(
        request,
        "expeditions/detail.html",
        {"expedition": expedition, "offres": offres},
    )
