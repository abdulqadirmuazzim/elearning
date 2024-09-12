from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Course, Student, Trainer


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    message = models.TextField(blank=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
