from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    profile_picture = models.ImageField(
        upload_to="static/students", default="static/assets/img/mylogo.png"
    )
    courses = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return self.user.username


# Replies to comments
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.reply}"

    def get_student(self):
        var = None
        for student in Student.objects.all():
            if self.user == student.user:
                var = student
        return var


# comments
class Course_Comment(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.TextField()
    replies = models.ManyToManyField(Reply, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name="comment_likes")
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment
