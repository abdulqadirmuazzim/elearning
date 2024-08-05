from django import forms
from .models import Contact as con, Subscription as subs, Student, Trainer, Course
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
        if not commit:
            user.save()
            Trainer.objects.create(
                user=user,
                bio=self.cleaned_data["bio"],
                passport_photo=self.cleaned_data["passport_photo"],
            )
        return user

    def save_form(self):
        pass


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
            if not commit:
                user.save()
                Student.objects.create(user=user)
            return user


# Student.courses.formfield()


class Course_Reg_form(forms.ModelForm):

    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check check-box"}),
    )

    class Meta:
        model = Student
        fields = ["courses"]


class Edit_Trainer(UserChangeForm):
    # create User form
    FirstName = forms.CharField(max_length=30, required=True)
    LastName = forms.CharField(max_length=30, required=True)
    UserName = forms.CharField(max_length=30, required=True)
    Email = forms.CharField(max_length=255, required=True)
    bio = forms.CharField(max_length=3000, required=True)

    class Meta:
        model = User
        fields = [
            "FirstName",
            "LastName",
            "UserName",
            "Email",
            "bio",
        ]


class Edit_Trainer_Passport(UserChangeForm):
    # create User form
    passport_photo = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ["passport_photo"]


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
