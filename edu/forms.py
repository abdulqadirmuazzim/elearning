from django import forms
from .models import Contact as con, Subscription as subs
from accounts.models import Course_Comment


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


# Course Comment from
class CourseComment_form(forms.ModelForm):
    class Meta:
        model = Course_Comment
        fields = ["comment"]
