from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from .models import Offre


# Register your models here.


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):

    autocomplete_fields = ('transporteur', 'expedition', 'vehicule')
    actions = ('accept_offres', 'refuse_offres')

    list_display = ('id', 'prix', 'date_proposition', 'delai_jours', 'statut_colore', 'transporteur', 'expedition', 'vehicule')
    list_filter = ('statut', 'date_proposition')
    search_fields = ('transporteur__raison_social', 'expedition__description', 'vehicule__immatriculation')
    ordering = ('-date_proposition',)
    date_hierarchy = 'date_proposition'
    list_per_page = 10

    fieldsets = (
        ('Informations générales', {
            'fields': ('prix', 'date_proposition', 'delai_jours', 'transporteur', 'expedition', 'vehicule')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
        ('Statut de l\'offre', {
            'fields': ('statut',)
        })
    )
    readonly_fields = ('date_proposition', 'created_at', 'updated_at')

    @admin.display(description='Statut de l\'offre')
    def statut_colore(self, obj):
        color = {
            'proposee': 'orange',
            'acceptee': 'green',
            'refusee': 'red',
            'retiree': 'gray',
        }.get(obj.statut, 'black')
        return format_html(
            (
                '<span style="display: inline-block; padding: 2px 8px; '
                'border-radius: 10px; background-color: {}; color: white; '
                'font-weight: 600;">{}</span>'
            ),
            color,
            obj.get_statut_display(),
        )

    @admin.action(description='Accepter les offres proposées')
    def accept_offres(self, request, queryset):
        updated = 0
        for offre in queryset.filter(statut='proposee'):
            offre.statut = 'acceptee'
            try:
                offre.save()
            except ValidationError as error:
                self.message_user(
                    request,
                    f'Offre {offre.pk}: {error}',
                    level=messages.ERROR,
                )
            else:
                updated += 1

        self._report_action_result(request, updated, 'acceptée(s)')

    @admin.action(description='Refuser les offres proposées')
    def refuse_offres(self, request, queryset):
        updated = queryset.filter(statut='proposee').update(
            statut='refusee'
        )
        self._report_action_result(request, updated, 'refusée(s)')

    def _report_action_result(self, request, updated, status):
        if updated:
            self.message_user(
                request,
                f'{updated} offre(s) {status}.',
                level=messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                "Aucune offre proposée n'a été mise à jour.",
                level=messages.WARNING,
            )
