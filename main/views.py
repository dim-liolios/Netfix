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


def login_view(request):
    # method is POST when the user has entered his credentials
    if request.method == "POST":
        form = UserLoginForm(request.POST)  # this form contains the submitted data from the user
        
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data["email"], password=form.cleaned_data["password"])
            # i) uses Django’s authentication system to verify credentials.
            # ii) returns a User object if credentials are valid; otherwise, returns None.
            if user:
                login(request, user)  # logs the user in
                return redirect("/")  # redirects to homepage logged in
            else:
                form.add_error(None, "Invalid email and/or password. If you don't have an account, you have to register first.")
        return render(request, "main/login_user.html", {"form": form})

    # else method is GET when the user first opens the page and no input has been passed
    else:
        form = UserLoginForm()  # create an empty form for GET requests
        return render(request, "main/login_user.html", {"form": form})

    # we imprort the users' login form from users/forms.py
