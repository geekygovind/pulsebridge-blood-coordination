from django.urls import path
from . import views

app_name = 'patient'
urlpatterns = [
    path('', views.patient_home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('donor/register/', views.donor_register, name='donor_register'),
    path('verify/', views.verify, name='verify'),
    path('availability/', views.availability, name='availability'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact, name='contact'),
]
