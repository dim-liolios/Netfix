from django import forms
  
from users.models import Company
from .models import Service


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price_hour = forms.DecimalField(max_digits=100, decimal_places=2)
    field = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        company_field = kwargs.pop("company_field", None)

        super().__init__(*args, **kwargs)

        if company_field == "All in One":
            self.fields["field"].choices = Service.choices
        else:
            self.fields["field"].choices = [(company_field, company_field)]

        # Adding placeholders to the fields
        self.fields["name"].widget.attrs["placeholder"] = "Enter Service Name"
        self.fields["description"].widget.attrs["placeholder"] = "Enter Description"
        self.fields["price_hour"].widget.attrs["placeholder"] = "Enter Price per Hour"

        self.fields["name"].widget.attrs["autocomplete"] = "off"
        self.fields["description"].widget.attrs["autocomplete"] = "off"
        self.fields["price_hour"].widget.attrs["autocomplete"] = "off"


class RequestService(forms.Form):
    address = forms.CharField(max_length=100)
    service_hours = forms.DecimalField(max_digits=100, decimal_places=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["address"].widget.attrs["placeholder"] = "Enter AddressDescription"
        self.fields["service_hours"].widget.attrs["placeholder"] = "Enter Service Hours"