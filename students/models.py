from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
class Hackathon(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.title
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    participated_hackathons = models.ManyToManyField(Hackathon, related_name='participants', blank=True)


    def __str__(self):
        return self.user.username




