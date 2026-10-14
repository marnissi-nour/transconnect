from django.contrib import admin
from .models import Expedition


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'date_souhaitee', 'statut')
    list_filter = ('statut', 'date_souhaitee')
    search_fields = ('reference',)
    list_editable = ('statut',)
    ordering = ('-date_souhaitee',)
    date_hierarchy = 'date_souhaitee'
    list_per_page=10

