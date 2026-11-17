from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.html import format_html

from .models import Expedition, ExpeditionEvenement, ExpeditionStatutHistorique


class ExpeditionStatutHistoriqueInline(admin.TabularInline):
    model = ExpeditionStatutHistorique
    extra = 0
    can_delete = False
    readonly_fields = ("ancien_statut", "nouveau_statut", "changed_by", "changed_at")


class ExpeditionEvenementInline(admin.TabularInline):
    model = ExpeditionEvenement
    extra = 0
    readonly_fields = ("created_by", "created_at")


class EnRetard(admin.SimpleListFilter):
    title = 'En retard'
    parameter_name = 'en_retard'

    def lookups(self, request, model_admin):
        return (
            ('oui', 'Oui'),
            ('non', 'Non'),
        )

    def queryset(self, request, queryset):
        date_filter = {
            'date_souhaitee__lt': timezone.localdate(),
            'statut__in': ['publiee', 'attribuee', 'en_cours'],
        }

        if self.value() == 'oui':
            return queryset.filter(**date_filter)
        if self.value() == 'non':
            return queryset.exclude(**date_filter)
        return queryset


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    inlines = (ExpeditionStatutHistoriqueInline, ExpeditionEvenementInline)

    list_display = (
        'reference',
        'ville_depart',
        'ville_arrive',
        'date_souhaitee',
        'statut_colore',
        'en_retard',
        'entreprise',
    )

    list_filter = ('statut', 'date_souhaitee', 'entreprise', EnRetard)
    search_fields = ('reference', 'ville_depart', 'ville_arrive', 'description', 'entreprise__raison_social')
    ordering = ('-date_souhaitee',)
    date_hierarchy = 'date_souhaitee'
    list_per_page = 10

    actions = ('make_it_livree',)

    fieldsets = (
        ('Informations générales', {
            'fields': (
                'reference',
                'ville_depart',
                'ville_arrive',
                'date_souhaitee',
                'poids_kg',
                'description',
                'entreprise',
                'statut',
            )
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('reference', 'created_at', 'updated_at')

    @admin.display(description='En retard')
    def en_retard(self, obj):
        if (
            obj.date_souhaitee < timezone.localdate()
            and obj.statut in ['publiee', 'attribuee', 'en_cours']
        ):
            return format_html(
                '<span style="display: inline-block; padding: 2px 8px; '
                'border-radius: 10px; background-color: red; color: white; '
                'font-weight: 600;">Oui</span>'
            )
        return format_html(
            '<span style="display: inline-block; padding: 2px 8px; '
            'border-radius: 10px; background-color: green; color: white; '
            'font-weight: 600;">Non</span>'
        )

    @admin.display(description='statut')
    def statut_colore(self, obj):
        color = {
            'publiee': 'blue',
            'attribuee': 'orange',
            'en_cours': 'green',
            'livree': 'gray',
            'annulee': 'red',
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

    @admin.action(description="Marquer comme livrée")
    def make_it_livree(self, request, queryset):
        expeditions = queryset.filter(statut='en_cours')
        updated = 0
        ingored = queryset.exclude(statut='en_cours')
        list_of_errors = []


        for expedition in expeditions:
            expedition.statut = 'livree'
            try:
                expedition.save()
                updated += 1
            except ValidationError as error:
                list_of_errors.append((expedition, error))
                self.message_user(
                    request,
                    f'{expedition}: {error}',
                    level=messages.ERROR,
                )
        if updated:
            self.message_user(
                request,
                f'{updated} expédition(s) marquée(s) comme livrée(s).',
                level=messages.SUCCESS,
            )
        if ingored:
            self.message_user(
                request,
                (
                    f"{len(ingored)} expédition(s) ignorée(s) car elles n'étaient "
                    "pas dans le statut 'En cours'."
                ),
                level=messages.WARNING,
            )
        if list_of_errors:
            self.message_user(
                request,
                (
                    f"{len(list_of_errors)} expédition(s) n'ont pas pu être "
                    "mise(s) à jour en raison d'erreurs de validation."
                ),
                level=messages.ERROR,
            )
