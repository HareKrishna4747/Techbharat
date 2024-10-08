# Generated by Django 5.0.7 on 2024-07-16 20:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0007_hackathon_participants"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hackathon",
            name="participants",
        ),
        migrations.AddField(
            model_name="student",
            name="participated_hackathons",
            field=models.ManyToManyField(
                blank=True, related_name="participants", to="students.hackathon"
            ),
        ),
    ]
