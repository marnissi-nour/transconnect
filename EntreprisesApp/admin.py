from django.contrib import admin
from django.utils.html import format_html
from .models import Utilisateur, Entreprise
from django.contrib.auth.admin import UserAdmin
from VehiculesApp.models import Vehicule

admin.site.site_header = "TransConnect Administration"
admin.site.site_title = "TransConnect Admin Portal"
admin.site.index_title = "Welcome to TransConnect Admin Portal"


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display=('user_id','role_colore','first_name','last_name')
    list_filter=('role', 'date_joined')
    search_fields=('user_id','first_name','last_name','email')
    list_editable=('first_name','last_name')
    ordering=('-created_at', )
    date_hierarchy='created_at'
    list_per_page=1

    @admin.display(description='Rôle')
    def role_colore(self, obj):
        colors = {
            'chargeur': 'blue',
            'transporteur': 'green',
            'administrateur': 'purple',
        }
        return format_html(
            '<span style="display: inline-block; padding: 2px 8px; '
            'border-radius: 10px; background-color: {}; color: white; '
            'font-weight: 600;">{}</span>',
            colors.get(obj.role, 'gray'),
            obj.get_role_display(),
        )

#admin.site.register(Utilisateur, UtilisateurAdmin)

class VehiculeInline(admin.TabularInline):
    model = Vehicule
    fields = ('immatriculation',)
    extra = 1


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    inlines = [VehiculeInline]
    list_display=('raison_social','type_colore','matricule_fiscal')
    list_filter=('raison_social',)
    search_fields=('raison_social','matricule_fiscal')

    fieldsets = (
        ('Identité de l\'entreprise', {
            'fields': ('raison_social', 'matricule_fiscal','type_entreprise')
        }), 
        ('Coordonnées', {
            'fields': ('adresse', 'gerant')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Type d’entreprise')
    def type_colore(self, obj):
        colors = {
            'chargeur': 'blue',
            'transporteur': 'green',
        }
        return format_html(
            '<span style="display: inline-block; padding: 2px 8px; '
            'border-radius: 10px; background-color: {}; color: white; '
            'font-weight: 600;">{}</span>',
            colors.get(obj.type_entreprise, 'gray'),
            obj.get_type_entreprise_display(),
        )







