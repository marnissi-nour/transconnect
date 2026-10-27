from django.urls import path

from . import views

app_name = "expeditions"

urlpatterns = [
    path("", views.list_expeditions, name="liste"),
    path("<str:reference>/", views.expedition_detail, name="detail"),
]