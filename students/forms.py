from django import forms
from django.contrib.auth.models import User
from .models import Student, Organizer, Hackathon,Skill


class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            student = Student.objects.create(user=user)
            student.skills.set(self.cleaned_data['skills'])
        return user

class OrganizerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Organizer.objects.create(user=user)
        return user

class HackathonForm(forms.ModelForm):
    class Meta:
        model = Hackathon
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from django.contrib.auth.models import User
from .models import Sponsor

class SponsorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Sponsor.objects.create(user=user)
        return user
from django import forms
from .models import Sponsorship

class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorship
        fields = ['amount', 'message']

from .models import Student, Organizer, Hackathon, Room
from django import forms
from .models import Room, Student

class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super(RoomCreationForm, self).__init__(*args, **kwargs)

        if student:
            # Exclude the creator from the list of students
            self.fields['students'] = forms.ModelMultipleChoiceField(
                queryset=Student.objects.filter(skills__in=student.skills.all()).exclude(id=student.id).distinct(),
                widget=forms.CheckboxSelectMultiple,
                required=False,
                label="Invite Students"
            )
        else:
            # If no student is provided, don't filter the queryset
            self.fields['students'] = forms.ModelMultipleChoiceField(
                queryset=Student.objects.all(),
                widget=forms.CheckboxSelectMultiple,
                required=False,
                label="Invite Students"
            )


class MembershipRequestForm(forms.Form):
    request_id = forms.IntegerField(widget=forms.HiddenInput)
    action = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('reject', 'Reject')],
        widget=forms.RadioSelect,
        label="Action"
    )