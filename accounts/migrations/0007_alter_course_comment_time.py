# Generated by Django 5.1.1 on 2024-09-13 23:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_student_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course_comment",
            name="time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
