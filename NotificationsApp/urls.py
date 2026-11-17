from django.urls import path

from .views import (
    NotificationListView,
    mark_all_notifications_read,
    mark_notification_read,
)

app_name = "notifications"

urlpatterns = [
    path("", NotificationListView.as_view(), name="liste"),
    path("<int:pk>/lue/", mark_notification_read, name="lire"),
    path("lire-tout/", mark_all_notifications_read, name="lire_tout"),
]
