from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Contact, Subscription


# fields that will show in the admin


class Con_display(admin.ModelAdmin):
    model = Contact
    list_display = ["Name", "Email", "Subject"]


class Sub_display(admin.ModelAdmin):
    model = Subscription
    list_display = ["Email"]


# User reg


# class RegisterAdmin(UserAdmin):
#     pass


admin.site.register(Contact, Con_display)

admin.site.register(Subscription, Sub_display)
