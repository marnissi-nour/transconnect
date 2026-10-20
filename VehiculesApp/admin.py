from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from .models import Vehicule


# Register your models here.

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = (
        'immatriculation',
        'type_vehicule',
        'capacite_kg',
        'statut_colore',
        'entreprise',
    )
    list_filter = ('type_vehicule', 'disponible', 'entreprise')
    search_fields = ('immatriculation', 'entreprise__raison_social')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 10

    fieldsets = (
        ('Informations générales', {
            'fields': ('immatriculation', 'type_vehicule', 'capacite_kg', 'entreprise')
        }),
        ('Statut de disponibilité', {
            'fields': ('disponible',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    @admin.action(description="Marquer comme disponible")
    def make_it_disponible(self, request, queryset):
        updated = queryset.filter(disponible=False).update(disponible=True)
        self._report_action_result(request, updated, 'disponible(s)')

    @admin.action(description="Marquer comme indisponible")
    def make_it_indisponible(self, request, queryset):
        updated = queryset.filter(disponible=True).update(disponible=False)
        self._report_action_result(request, updated, 'indisponible(s)')

    actions = ('make_it_disponible', 'make_it_indisponible')

    def _report_action_result(self, request, updated, status):
        if updated:
            self.message_user(
                request,
                f'{updated} véhicule(s) marqué(s) comme {status}.',
                level=messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                "Aucun véhicule n'a été mis à jour.",
                level=messages.WARNING,
            )

    @admin.display(description='Statut de disponibilité')
    def statut_colore(self, obj):
        color = 'green' if obj.disponible else 'red'
        return format_html(
            (
                '<span style="display: inline-block; padding: 2px 8px; '
                'border-radius: 10px; background-color: {}; color: white; '
                'font-weight: 600;">{}</span>'
            ),
            color,
            'Disponible' if obj.disponible else 'Indisponible',
        )
