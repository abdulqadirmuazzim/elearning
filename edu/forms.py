from django import forms
from .models import Contact as con, Subscription as subs, Student, Trainer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


# trainer reg form
class TrainerForm(UserCreationForm):
    # create User form
    FirstName = forms.CharField(max_length=30, required=True)
    LastName = forms.CharField(max_length=30, required=True)
    UserName = forms.CharField(max_length=30, required=True)
    Email = forms.CharField(max_length=255, required=True)
    bio = forms.CharField(max_length=3000, required=True)
    passport_photo = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = [
            "FirstName",
            "LastName",
            "UserName",
            "Email",
            "bio",
            "passport_photo",
            "password1",
            "password2",
        ]

        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data["email"]
            if not commit:
                user.save()
                Trainer.objects.create(
                    user=user,
                    bio=self.cleaned_data["bio"],
                    passport_photo=self.cleaned_data["passport_photo"],
                )
            return user


# trainer reg form
class StudentForm(UserCreationForm):
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

        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data["email"]
            if not commit:
                user.save()
                Student.objects.create(user=user)
            return user


class Edit_Trainer(UserChangeForm):
    # create User form
    FirstName = forms.CharField(max_length=30, required=True)
    LastName = forms.CharField(max_length=30, required=True)
    UserName = forms.CharField(max_length=30, required=True)
    Email = forms.CharField(max_length=255, required=True)
    bio = forms.CharField(max_length=3000, required=True)
    passport_photo = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = [
            "FirstName",
            "LastName",
            "UserName",
            "Email",
            "bio",
            "passport_photo",
        ]


# contact form
class comment(forms.ModelForm):
    class Meta:
        model = con
        fields = ["Name", "Email", "Subject", "Message"]


# subscription form
class subscription(forms.ModelForm):
    class Meta:
        model = subs
        fields = ["Email"]
