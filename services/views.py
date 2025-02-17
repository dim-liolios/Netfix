from django.shortcuts import render, redirect, get_object_or_404

from users.models import Company
from services.models import Service, RequestService

from services.forms import CreateNewService, RequestServiceForm


def list_of_services(request):
    services = Service.objects.all().order_by("-date")
    return render(request, "services/list_of_services.html", {"services": services})


def single_service(request, id):
    service = Service.objects.get(id=id)  # get the service by ID
    return render(request, "services/single_service.html", {"service": service})


def create_service(request):
    if request.method == "POST":
        # if the request is POST, this creates an instance of CreateNewService form
        # with all the data input from the user

        company = Company.objects.get(user=request.user)
        company_field = company.field

        #  the request.POST contains all the data submitted by the user
        form = CreateNewService(request.POST, company_field=company_field)
        if form.is_valid():
            # if the form is valid a new Service object is created and saved to the database
            Service.objects.create(
                company=company,
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                price_hour=form.cleaned_data["price_hour"],
                field=form.cleaned_data["field"],
            )
            return redirect("services_list")
        # else:
        #     print(form.errors)
    else:
        company = Company.objects.get(user=request.user)
        company_field = company.field
        form = CreateNewService(company_field=company_field)

    return render(request, "services/create_service.html", {"form": form})


def services_per_field(request, field):
    # search for the service present in the url
    field = field.replace("-", " ").title()
    services = Service.objects.filter(field=field)
    return render(request, "services/services_per_field.html", {"services": services, "field": field})


def request_service(request, id):
    service = get_object_or_404(Service, pk=id)

    if request.method == "POST":
        form = RequestServiceForm(request.POST)

        if form.is_valid():
            customer = request.user.customer
            service_hours = form.cleaned_data["service_hours"]

            calculated_cost = service.price_hour * service_hours

            RequestService.objects.create(
                service=service,
                customer=customer,
                calculated_cost=calculated_cost,
                service_hours=service_hours,
                company=service.company,
            )

            return redirect("customer_profile", name=request.user.username)
            # in redirect() the first argument should be a view:
            # using "return redirect("customer_profile", name=request.user.username), we are
            # telling Django to use the name of the view ("customer_profile" or "company_profile")
            # and resolve the full URL for that view dynamically. Django will use the URL pattern
            # associated with that view name and generate the corresponding URL using the parameters
            # (like name=request.user.username) you provide.
            # This does NOT work: "return redirect("customer/<slug:name>", name=request.user.username)"
            # in login form we can use "return redirect("/") because we tell Django to serve
            # a static (home) page

    else:
        form = RequestServiceForm()

    return render(request, "services/request_service.html", {"form": form, "service": service})
