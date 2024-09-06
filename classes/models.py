from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Course, Student, Trainer


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    comment = models.TextField()
    date_commented = models.DateTimeField(auto_now=True)


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    message = models.TextField(blank=True)
    time = models.DateTimeField(auto_now=True)
