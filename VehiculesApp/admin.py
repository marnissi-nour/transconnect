from django.contrib import admin
from .models import Vehicule


# Register your models here.

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible', 'entreprise')
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
