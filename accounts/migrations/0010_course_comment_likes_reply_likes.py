# Generated by Django 5.1.1 on 2024-09-22 01:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0009_remove_reply_comment_course_comment_replies"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="course_comment",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="comment_likes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="reply",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
