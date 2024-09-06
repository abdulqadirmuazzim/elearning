from django.db import models
from django.contrib.auth.models import User


# Let's create a model for the instructors and courses


# trainers
class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    passport_photo = models.ImageField(upload_to="static/img/")
    likes = models.ManyToManyField(User, blank=True, related_name="trainer_likes")

    def __str__(self):
        return str(self.user)


# courses
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    cover_photo = models.ImageField(upload_to="static/img/")
    description = models.TextField()
    # students = models.ManyToManyField(User, blank=True)
    price = models.FloatField()
    likes = models.ManyToManyField(User, blank=True, related_name="course_likes")

    def __str__(self):
        return self.course_name


# students
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, blank=True)
