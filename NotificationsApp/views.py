from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import View

from .models import Notification


def _notifications_for(user):
    return Notification.objects.filter(destinataire=user).select_related(
        "offre",
        "offre__expedition",
    )


class NotificationListView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            "notifications/liste.html",
            {"notifications": _notifications_for(request.user)},
        )


@require_POST
@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        destinataire=request.user,
    )
    notification.lue = True
    notification.save(update_fields=["lue"])
    return redirect("notifications:liste")


@require_POST
@login_required
def mark_all_notifications_read(request):
    _notifications_for(request.user).filter(lue=False).update(lue=True)
    return redirect("notifications:liste")
