from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import CreateView, TemplateView
import logging

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User

logger = logging.getLogger(__name__)

# =================================================================================================


# CHOOSE TYPE OF USER TO REGISTER
def register(request):
    return render(request, "users/register.html")


# the following 2 classes work as the previous login function but for register. The reason
# we use a class instead of a function while calling the appropriate form (class),is that
# the registration process is more complicated
# | | |
# v v v

# =================================================================================================


# CUSTOMER REGISTRATION
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = "users/register_customer.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "customer"
        return super().get_context_data(**kwargs)
        # this is used to add extra information to the context that will be passed to
        # the template (user = customer)

    def form_valid(self, form):  # this form argument is the validated instance of the CustomerSignUpForm
        user = form.instance
        login(self.request, user)  # he is immediatly logged in here
        return redirect("/")


# =================================================================================================


# COMPANY REGISTRATION
class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = "users/register_company.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "company"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            logger.info("✅ Form is valid!")
            user = form.save()
            logger.info(f"✅ User saved: {user.username}")
            login(self.request, user)
            return redirect("/")
        else:
            logger.error("❌ Form errors: %s", form.errors)
            return self.form_invalid(form)
