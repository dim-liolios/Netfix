from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout

from users.forms import UserLoginForm


def home(request):
    return render(request, "main/home.html", {})
    # {}: empty dictionary, means the template will render without any dynamic data
    # (it will just be static content), we can skip this


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
    # django_logout(request): used to log out the current user from the session,
    # essentially ending their authentication session


def login(request):
    # method is POST when the user has entered his credentials
    if request.method == "POST":
        form = UserLoginForm(request.POST)  # this form contains the submitted data from the user
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)  # logs the user in
            return redirect("/")  # redirects to homepage
        
    # else method is GET when the user first opens the page and no input has been passed
    else:
        form = UserLoginForm()  # Create an empty form for GET requests
        return render(request, "main/login_user.html", {"form": form})

    # we imprort the users' login form from users app -> forms.py
