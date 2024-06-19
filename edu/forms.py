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
        if User.objects.filter(username_iexact=user).exists():
            raise forms.ValidationError("Username already taken")
        return user

        # clean the email

    def clean_email(self):
        email = self.cleaned_data["Email"]
        if User.objects.filter(email_iexact=email).exists():
            raise forms.ValidationError("Email already in use")
        return email

    # def save(self, *args, **kwargs):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password'])
    #     if commit:
    #         user.save()
    #         if hasattr(self, 'save_m2m'):
    #             self.save_m2m()
    #     return user


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
