from django.contrib import admin
from .models import Utilisateur, Entreprise

from django.contrib.auth.admin import UserAdmin

@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display=('user_id','role','first_name','last_name')
    list_filter=('role', 'date_joined')
    search_fields=('user_id','first_name','last_name','email')
    list_editable=('role','first_name','last_name')
    ordering=('-created_at', )
    date_hierarchy='created_at'
    list_per_page=1

#admin.site.register(Utilisateur, UtilisateurAdmin)



@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display=('raison_social','matricule_fiscal')
    list_filter=('raison_social',)
    search_fields=('raison_social','matricule_fiscal')
    
    









