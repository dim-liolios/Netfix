from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = "date"


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    pass


class CompanySignUpForm(UserCreationForm):
    field_of_work = forms.ChoiceField(
        choices=Company._meta.get_field("field").choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email", "field_of_work"]
        # thats the order the fields appear in the form but ONLY when i use {{ form }} in html

    def __init__(self, *args, **kwargs):
        super(CompanySignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control", "placeholder": "Enter username"})
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Enter email"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Enter password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Re-enter same password"})

        self.fields["email"].widget.attrs["autocomplete"] = "off"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True

        if commit:
            user.save()  # saving the user instance (making a User Class object)
            Company.objects.create(user=user, field=self.cleaned_data["field_of_work"])
            # creating the company instance and link it to the user

        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"}))
    # Django built-in authenticate() uses username and password, not email

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["autocomplete"] = "off"
        # tells browsers not to suggest previously entered emails

    def clean(self):
        cleaned_data = super().clean()  # => method of parent class forms.Form that returns
        # a dictionary where keys are the "email", "pass" etc and values the user's inputs
        return cleaned_data

    # clean(self) ensures the form is valid as a whole, while Django’s built-in validation
    # (super.clean()) ensures each field is valid individually
