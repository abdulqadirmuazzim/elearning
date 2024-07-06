from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Contact, Subscription, Student, Trainer, Course


# fields that will show in the admin


class Con_display(admin.ModelAdmin):
    model = Contact
    list_display = ["Name", "Email", "Subject"]


class Sub_display(admin.ModelAdmin):
    model = Subscription
    list_display = ["Email"]


class Course_display(admin.ModelAdmin):
    model = Course
    list_display = ["course_name", "cover_photo", "trainer", "price"]


class StudentDisplay(admin.ModelAdmin):
    model = Student
    list_display = ["user", "courses"]


class TrainerDisplay(admin.ModelAdmin):
    model = Trainer
    list_display = ["user"]


# User reg


# class RegisterAdmin(UserAdmin):
#     pass


admin.site.register(Contact, Con_display)

admin.site.register(Student, StudentDisplay)

admin.site.register(Trainer, TrainerDisplay)

admin.site.register(Subscription, Sub_display)

admin.site.register(Course, Course_display)
