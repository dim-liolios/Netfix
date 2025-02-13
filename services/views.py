from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from users.models import Company, Customer, User

from .models import Service
from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, "services/list.html", {"services": services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, "services/single_service.html", {"service": service})


def create(request):
    if request.method == "POST":
        # if the request is POST, this creates an instance of CreateNewService form
        #  the request.POST contains all the data submitted by the user
        form = CreateNewService(request.POST)
        if form.is_valid():
            # if the form is valid a new Service object is created and saved to the database
            Service.objects.create(
                company=Company.objects.get(user=request.user),
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                price_hour=form.cleaned_data["price_hour"],
                field=form.cleaned_data["field"],
            )
            return redirect("services_list")
    else:
        form = CreateNewService(choices=Service.choices)

    return render(request, "services/create.html", {"form": form})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace("-", " ").title()
    services = Service.objects.filter(field=field)
    return render(request, "services/field.html", {"services": services, "field": field})


def request_service(request, id):
    return render(request, "services/request_service.html", {})
