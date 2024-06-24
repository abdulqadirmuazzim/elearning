from django import forms
from .models import Contact as con, Subscription as subs
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# reg form
class register(UserCreationForm):
    # create User form
    FirstName = forms.CharField(max_length=30, required=True)
    LastName = forms.CharField(max_length=30, required=True)
    UserName = forms.CharField(max_length=30, required=True)
    Email = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = [
            "FirstName",
            "LastName",
            "UserName",
            "Email",
            "password1",
            "password2",
        ]
        # clean the username

    def clean_username(self):
        user = self.cleaned_data["UserName"]
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError("Username already taken")
        return user

        # clean the email

    def clean_email(self):
        email = self.cleaned_data["Email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use")
        return email


# contact form
class comment(forms.ModelForm):
    class Meta:
        model = con
        fields = ["Name", "Email", "Subject", "Message"]


# subscription form
class subsrciption(forms.ModelForm):
    class Meta:
        model = subs
        fields = "__all__"
