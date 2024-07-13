from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager, User

from django.db.models.signals import post_save
from django.dispatch import receiver


# Contact Form
class Contact(models.Model):
    Name = models.CharField(max_length=255)
    Subject = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    Message = models.CharField(max_length=500)
    date_created = models.DateTimeField(default=timezone.datetime.now)


# Subscriptions
class Subscription(models.Model):
    Email = models.EmailField(max_length=255)
    date_created = models.DateTimeField(default=timezone.datetime.now)


# Let's create a model for the instructors and courses


# trainers
class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    passport_photo = models.ImageField(upload_to="static/img/")

    def __str__(self):
        return str(self.user)


# courses
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    cover_photo = models.ImageField(upload_to="static/img/")
    price = models.FloatField()

    def __str__(self):
        return self.course_name


# students
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)


# Instructors and students
# class User(AbstractUser):
#     class Role(models.TextChoices):
#         ADMIN = "ADMIN", "admin"
#         TRAINER = "TRAINER", "Trainer"
#         STUDENT = "STUDENT", "Studen"

#     base_role = Role.ADMIN

#     role = models.CharField(max_length=50, choices=Role.choices)

#     # override the save method
#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.role = self.base_role
#             return super().save(*args, **kwargs)


# # managers


# # for students


# # Student manager
# class StudentManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role=User.Role.STUDENT)


# class Student(User):
#     base_role = User.Role.STUDENT
#     student = StudentManager()

#     class Meta:
#         proxy = True


# @receiver(post_save, sender=Student)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "STUDENT":
#         StudentProfile.objects.create(user=instance)


# # student profile
# class StudentProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     student_id = models.IntegerField(null=True, blank=True)


# # for trainers


# # Trainer Manager
# class TrainerManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role=User.Role.TRAINER)


# class Trainer(User):
#     base_role = User.Role.TRAINER
#     trainer = TrainerManager()

#     class Meta:
#         proxy = True
