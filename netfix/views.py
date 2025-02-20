from django.shortcuts import render

from users.models import User, Company, Customer
from services.models import Service, RequestService


def home(request):
    return render(request, "users/home.html", {"user": request.user})


def customer_profile(request, name):
    user = User.objects.get(username=name)

    customer = Customer.objects.get(user=user)

    requested_services = RequestService.objects.filter(customer=customer).order_by("-requested_date")

    return render(request, "users/profile.html", {"user": user, "requested_services": requested_services})


def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(company=Company.objects.get(user=user)).order_by("-date")

    return render(request, "users/profile.html", {"user": user, "services": services})
