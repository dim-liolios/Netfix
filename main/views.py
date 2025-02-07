from django.shortcuts import render
from django.contrib.auth import logout as django_logout


def home(request):
    return render(request, "main/home.html", {})

# {}: empty dictionary, means the template will render without any dynamic data (it will just be static content)

def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")

# django_logout(request): used to log out the current user from the session, essentially ending their authentication session
