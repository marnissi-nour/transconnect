from django.contrib import admin
from .models import Offre


# Register your models here.


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'prix', 'date_proposition', 'delai_jours', 'statut', 'transporteur', 'expedition', 'vehicule')
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
    readonly_fields = ('created_at', 'updated_at')
