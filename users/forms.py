from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer

# class DateInput(forms.DateInput):
#     input_type = "date"


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

        self.fields["username"].widget.attrs["autocomplete"] = "off"
        self.fields["email"].widget.attrs["autocomplete"] = "off"

    # Django automatically calls any method in the form that starts with clean_, even custom ones.
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

    # the save() method, custom ones or the default from the parent class never runs
    # unless is called in the form view
    def save(self, commit=True):
        user = super().save(commit=False)
        # calling the parent class’s save functionality first (UserCreationForm class's validation,
        # field processing, and password handling), and then modify the object
        # (like setting is_company = True) before it’s actually saved in the "if commit:" part below
        user.is_company = True

        if commit:
            user.save()  # saving the user as Company
            print(f"✅ User saved: {user.username}")
            Company.objects.create(user=user, field=self.cleaned_data["field_of_work"])
            # creating the company instance and link it to the user
            print("✅ Company created!")

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
