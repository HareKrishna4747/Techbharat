# students/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, OrganizerRegistrationForm, HackathonForm
from .models import Hackathon  # Assuming you have a Hackathon model
from django.shortcuts import get_object_or_404
from .models import Organizer
from .forms import HackathonForm 
from django.contrib.auth import logout
from .models import Organizer
from .models import Hackathon

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_home')
        else:
            print(form.errors)
    else:
        form = StudentRegistrationForm()
    return render(request, 'students/register_student.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import OrganizerRegistrationForm

def register_organizer(request):
    if request.method == 'POST':
        form = OrganizerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the form data and return the user object
            login(request, user)  # Log in the user
            # Extract the username from the user object and use it in the redirect
            return redirect('organizer_home', username=user.username)  # Redirect to organizer home upon successful registration
    else:
        form = OrganizerRegistrationForm()
    
    return render(request, 'students/register_organizer.html', {'form': form})


@login_required  # Ensures only authenticated users can access this view
def student_home(request):
    return render(request, 'students/student_home.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Organizer

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'student'):
            return redirect('student_home')
        elif hasattr(request.user, 'organizer'):
            organizer = Organizer.objects.get(user=request.user)
            return redirect('organizer_home', username=organizer.user.username)
        elif hasattr(request.user, 'sponsor'):
            return redirect('sponsor_home')
        else:
            return redirect('home')
    else:
        return redirect('home')

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

def hackathon_list(request):
    hackathons = Hackathon.objects.all()  # Adjust this query as needed
    return render(request, 'students/hackathon_list.html', {'hackathons': hackathons})


@login_required
def add_hackathon(request):
    if request.method == 'POST':
        form = HackathonForm(request.POST)
        if form.is_valid():
            hackathon = form.save(commit=False)
            hackathon.organizer = get_object_or_404(Organizer, user=request.user)
            hackathon.save()
            return redirect('hackathon_list')
    else:
        form = HackathonForm()

    return render(request, 'students/add_hackathon.html', {'form': form,'username': request.user.username })

@login_required
def organizer_home(request, username):
    return render(request, 'students/organizer_home.html', {'username': username})
from django.shortcuts import render
from .models import Hackathon  # Import your Hackathon model

def hackathon_list(request):
    hackathons = Hackathon.objects.all()  # Fetch all Hackathon objects
    return render(request, 'students/hackathon_list.html', {'hackathons': hackathons})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home') 


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Hackathon, Student

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Hackathon, Student

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Hackathon, Student

@login_required
@csrf_exempt
def participate_in_hackathon(request, hackathon_id):
    if request.method == 'POST':
        hackathon = get_object_or_404(Hackathon, id=hackathon_id)
        student = Student.objects.get(user=request.user)
        hackathon.participants.add(student)
        hackathon.save()
        return JsonResponse({'message': 'Participation successful'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Hackathon, Student

@login_required
def participated_hackathons(request):
    student = get_object_or_404(Student, user=request.user)
    participated_hackathons = student.participated_hackathons.all()
    return render(request, 'participated_hackathons.html', {'participated_hackathons': participated_hackathons})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Hackathon, Organizer

@login_required
def my_hackathons(request):
    organizer = Organizer.objects.get(user=request.user)
    hackathons = Hackathon.objects.filter(organizer=organizer)
    return render(request, 'my_hackathons.html', {'hackathons': hackathons})


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Hackathon, Student

@login_required
def back_off_hackathon(request, hackathon_id):
    hackathon = get_object_or_404(Hackathon, id=hackathon_id)
    student = get_object_or_404(Student, user=request.user)
    if hackathon in student.participated_hackathons.all():
        student.participated_hackathons.remove(hackathon)
    return redirect('participated_hackathons')

# views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View
from .models import Hackathon

class CancelHackathonView(View):
    def post(self, request, pk):
        hackathon = get_object_or_404(Hackathon, pk=pk, organizer=request.user.organizer)
        hackathon.delete()
        messages.success(request, 'Hackathon deleted successfully.')
        return redirect('my_hackathons')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Organizer, Sponsor

@login_required
def sponsor_home(request):
    # Assuming you want to pass some data to the sponsor home template
    context = {
        'sponsor': request.user.sponsor,
    }
    return render(request, 'sponsor_home.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SponsorRegistrationForm

def register_sponsor(request):
    if request.method == 'POST':
        form = SponsorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('sponsor_home')
    else:
        form = SponsorRegistrationForm()
    return render(request, 'register_sponsor.html', {'form': form})
