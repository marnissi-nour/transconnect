from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("message", "destinataire", "offre", "lue", "created_at")
    list_filter = ("lue", "created_at")
    search_fields = ("message", "destinataire__username")
    readonly_fields = ("created_at",)
