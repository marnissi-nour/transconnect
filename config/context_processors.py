from NotificationsApp.models import Notification


def notifications(request):
    if not request.user.is_authenticated:
        return {
            "unread_notifications_count": 0,
            "unread_notifications": [],
        }

    unread = Notification.objects.filter(
        destinataire=request.user,
        lue=False,
    )
    return {
        "unread_notifications_count": unread.count(),
        "unread_notifications": unread.select_related(
            "offre",
            "offre__expedition",
        )[:3],
    }
