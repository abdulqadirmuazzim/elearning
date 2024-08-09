from django.contrib import admin
from .models import Student, Trainer, Course


# fields that will show in the admin




class Course_display(admin.ModelAdmin):
    model = Course
    list_display = ["course_name", "cover_photo", "trainer", "price"]


class StudentDisplay(admin.ModelAdmin):
    model = Student
    list_display = ["user"]


class TrainerDisplay(admin.ModelAdmin):
    model = Trainer
    list_display = ["user"]


admin.site.register(Student, StudentDisplay)

admin.site.register(Trainer, TrainerDisplay)

admin.site.register(Course, Course_display)
