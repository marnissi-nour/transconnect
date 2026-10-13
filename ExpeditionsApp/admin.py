from django.contrib import admin
from .models import Expedition 

# Register your models here.


@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'date_souhaitee', 'ville_depart', 'ville_arrive')
    search_fields = ('description', 'ville_depart', 'ville_arrive')
    ordering = ('-date_souhaitee',)
    date_hierarchy = 'date_souhaitee'
    list_per_page = 10




