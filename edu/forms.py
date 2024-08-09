from django import forms
from .models import Contact as con, Subscription as subs


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
