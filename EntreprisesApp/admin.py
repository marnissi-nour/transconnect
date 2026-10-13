from django.contrib import admin
from .models import Utilisateur, Entreprise
from django.contrib.auth.admin import UserAdmin

admin.site.register(Entreprise)





@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display=('user_id','role','first_name','last_name')
    list_filter=('role', 'date_joined')
    search_fields=('user_id','first_name','last_name','email')

    


#admin.site.register(Utilisateur, UtilisateurAdmin)


