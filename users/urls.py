from django.urls import path
from django.contrib.auth import views

from .forms import UserLoginForm
from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("login/", views.LoginUserView.as_view(), name="login_user"),
    path("company/", views.CompanySignUpView.as_view(), name="register_company"),
    path("customer/", views.CustomerSignUpView.as_view(), name="register_customer"),
]
