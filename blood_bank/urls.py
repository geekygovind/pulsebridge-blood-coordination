from django.urls import path
from . import views

app_name = 'blood_bank'
urlpatterns = [
    path('', views.home, name='home'),
    path('availability/', views.availability, name='availability'),
    path('inventory/add/', views.update, name='update'),
    path('requests/', views.pending_requests, name='pending_requests'),
    path('requests/<int:request_id>/accept/', views.accept_request, name='accept_request'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
]
