from django.http import HttpResponse





def index(request,nom):
    return HttpResponse(f" <h1>Welcome to home page, {nom}.</h1>")



