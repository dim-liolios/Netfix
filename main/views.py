from django.shortcuts import render
from django.contrib.auth import logout as django_logout

from users.forms import UserLoginForm


def home(request):
    return render(request, "main/home.html", {})
    # {}: empty dictionary, means the template will render without any dynamic data (it will just be static content), we can skip this


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
    # django_logout(request): used to log out the current user from the session, essentially ending their authentication session


def login(request):
    login_form = UserLoginForm()
    return render(request, "main/login_user.html", {"form": login_form})
    # we imprort the users' login form from users app, forms.py
