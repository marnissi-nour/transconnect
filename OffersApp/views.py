from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Offre


def liste_offres(request):
    offres = Offre.objects.select_related(
        "transporteur", "expedition", "vehicule"
    ).order_by("-date_proposition")
    return render(request, "offres/liste.html", {"offres": offres})


def detail_offre(request, pk):
    offre = get_object_or_404(
        Offre.objects.select_related(
            "transporteur", "expedition", "vehicule"
        ),
        pk=pk,
    )
    return render(request, "offres/detail.html", {"offre": offre})


@require_http_methods(["GET", "POST"])
def supprimer_offre(request, pk):
    offre = get_object_or_404(Offre, pk=pk)
    if request.method == "POST":
        offre.delete()
        return HttpResponseRedirect(reverse("offres:liste"))
    return render(
        request,
        "offres/confirmer_suppression.html",
        {"objet": offre},
    )
