from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def index(request, nom):
    return render(request, "home.html", {"name": nom})
