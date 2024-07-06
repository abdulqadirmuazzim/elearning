from django.db.models.signals import post_save, connection_created
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Trainer, Student


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance, "trainer"):
            Trainer.objects.create(user=instance)
        if hasattr(instance, "student"):
            Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "trainer"):
        instance.trainerprofile.save()
    if hasattr(instance, "student"):
        instance.studentprofile.save()


# In your Django app (e.g., signals.py or any other module)s


@receiver(connection_created)
def set_autocommit(sender, connection, **kwargs):
    connection.cursor().execute("SET autocommit=1")
