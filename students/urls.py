from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import participate_in_hackathon,my_hackathons,CancelHackathonView,sponsor_hackathon, withdraw_sponsorship,sponsored_hackathons
urlpatterns = [
    path('', views.home, name='home'),
    path('student_home/', views.student_home, name='student_home'),
    path('login/student/', auth_views.LoginView.as_view(template_name='login_student.html'), name='login_student'),
    path('login/organizer/', auth_views.LoginView.as_view(template_name='login_organizer.html'), name='login_organizer'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('hackathons/', views.hackathon_list, name='hackathon_list'),
    path('organizer_home/<str:username>/', views.organizer_home, name='organizer_home'),
    path('register/register_organizer/', views.register_organizer, name='register_organizer'),
    path('add_hackathon/', views.add_hackathon, name='add_hackathon'),
    path('register/register_student/', views.register_student, name='register_student'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('participate/<int:hackathon_id>/', participate_in_hackathon, name='participate_in_hackathon'),
    path('participated_hackathons/', views.participated_hackathons, name='participated_hackathons'),
    path('my_hackathons/', views.my_hackathons, name='my_hackathons'),
    path('back_off_hackathon/<int:hackathon_id>/', views.back_off_hackathon, name='back_off_hackathon'),
    path('cancel_hackathon/<int:pk>/', CancelHackathonView.as_view(), name='cancel_hackathon'),
    path('sponsor_home/', views.sponsor_home, name='sponsor_home'),
    path('login/sponsor/', auth_views.LoginView.as_view(template_name='login_sponsor.html'), name='login_sponsor'),
    path('register/register_sponsor/', views.register_sponsor, name='register_sponsor'),
    path('sponsor_hackathon/<int:hackathon_id>/', views.sponsor_hackathon, name='sponsor_hackathon'),
    path('withdraw_sponsorship/<int:hackathon_id>/', withdraw_sponsorship, name='withdraw_sponsorship'),
    path('sponsored_hackathons/', sponsored_hackathons, name='sponsored_hackathons'),


]
