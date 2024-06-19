from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Contact, Subscription
from .forms import register


# fields that will show in the admin


class Con_display(admin.ModelAdmin):
    model = Contact
    list_display = ["Name", "Email", "Subject"]


# User reg


# class RegisterAdmin(UserAdmin):
#     pass


admin.site.register(Contact, Con_display)
# admin.site.register(RegisterAdmin)

admin.site.register(Subscription)
