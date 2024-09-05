from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Sponsor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sponsored_hackathons = models.ManyToManyField('Hackathon', related_name='sponsors')

    

    def __str__(self):
        return self.user.username

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




from django.db import models
from django.contrib.auth.models import User

class Sponsorship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default = 100)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hackathon')

    def __str__(self):
        return f"{self.user.username} sponsoring {self.hackathon.title}"


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='created_rooms')
    members = models.ManyToManyField(Student, related_name='rooms', through='RoomMembership')

    def __str__(self):
        return self.name

class RoomMembership(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    date_requested = models.DateTimeField(default=timezone.now)
    date_approved = models.DateTimeField(blank=True, null=True)

    def approve(self):
        self.is_approved = True
        self.date_approved = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.student.user.username} - {self.room.name}"


from django.db import models
from .models import Room, Student

class MembershipRequest(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.student} - {self.room}'
