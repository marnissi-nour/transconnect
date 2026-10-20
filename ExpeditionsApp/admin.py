from django.contrib import admin
from .models import Expedition


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'ville_depart', 'ville_arrive', 'date_souhaitee', 'statut', 'entreprise')
    list_filter = ('statut', 'date_souhaitee', 'entreprise')
    search_fields = ('reference', 'ville_depart', 'ville_arrive', 'description', 'entreprise__raison_social')
    list_editable = ('statut',)
    ordering = ('-date_souhaitee',)
    date_hierarchy = 'date_souhaitee'
    list_per_page = 10

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
