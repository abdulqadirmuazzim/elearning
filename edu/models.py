from django.db import models
from django.utils import timezone


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
