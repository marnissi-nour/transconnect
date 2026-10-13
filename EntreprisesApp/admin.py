from django.contrib import admin
from .models import Utilisateur, Entreprise


admin.site.register(Utilisateur)
admin.site.register(Entreprise)