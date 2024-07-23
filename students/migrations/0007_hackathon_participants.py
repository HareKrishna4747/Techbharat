# Generated by Django 5.0.7 on 2024-07-16 19:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0006_alter_hackathon_organizer_alter_organizer_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="hackathon",
            name="participants",
            field=models.ManyToManyField(
                related_name="hackathons", to="students.student"
            ),
        ),
    ]
