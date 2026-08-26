from django.urls import path
from . import views

app_name = 'hospital'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('availability/', views.availability, name='availability'),
    path('requests/new/', views.request_blood, name='request_blood'),
]
