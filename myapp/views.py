from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Sum
from django.shortcuts import redirect, render

from blood_bank.models import BloodUnit
from .models import Donor, Patient


def home(request):
    return render(request, 'index.html')


def patient_home(request):
    return render(request, 'patient/home.html', {'active_page': 'home'})


def login_user(request):
    return render(request, 'patient/login.html', {'active_page': 'login'})


def about_page(request):
    return render(request, 'patient/about.html', {'active_page': 'about'})


def contact(request):
    return render(request, 'patient/contact.html', {'active_page': 'contact'})


def availability(request):
    city = request.GET.get('city', '').strip()
    blood_group = request.GET.get('blood_group', '').strip()
    try:
        units_required = max(1, int(request.GET.get('units', '1')))
    except ValueError:
        units_required = 1
    inventory = BloodUnit.objects.filter(status='AVAILABLE')
    if city:
        inventory = inventory.filter(blood_bank__city__iexact=city)
    if blood_group:
        inventory = inventory.filter(blood_group=blood_group)
    results = inventory.values('blood_bank__name', 'blood_bank__area', 'blood_bank__city', 'blood_group').annotate(total_units=Sum('units')).filter(total_units__gte=units_required).order_by('blood_bank__name')
    cities = BloodUnit.objects.exclude(blood_bank__city='').values_list('blood_bank__city', flat=True).distinct().order_by('blood_bank__city')
    return render(request, 'patient/availability.html', {'active_page': 'availability', 'results': results, 'cities': cities, 'selected_city': city, 'selected_blood_group': blood_group, 'units_required': units_required, 'searched': bool(city or blood_group)})


def register(request):
    if request.method == 'POST':
        name, area, city = (request.POST.get(key, '').strip() for key in ('name', 'area', 'city'))
        contact, password = request.POST.get('contact', '').strip(), request.POST.get('password', '')
        if not all([name, area, city, contact, password]):
            messages.error(request, 'Please complete every field.')
        elif Patient.objects.filter(name__iexact=name).exists():
            messages.error(request, 'An account with that name already exists. Please log in.')
        else:
            Patient.objects.create(name=name, area=area, city=city, contact_no=contact, password=make_password(password))
            messages.success(request, 'Registration complete. Please log in.')
            return redirect('patient:login')
    return render(request, 'patient/register.html', {'active_page': 'register'})


def donor_register(request):
    if request.method == 'POST':
        name, blood_group, city = (request.POST.get(key, '').strip() for key in ('name', 'blood_group', 'city'))
        contact = request.POST.get('contact', '').strip()
        if not all([name, blood_group, city, contact]):
            messages.error(request, 'Please complete all donor details.')
        else:
            Donor.objects.create(name=name, blood_group=blood_group, city=city, contact_no=contact, last_donation_date=request.POST.get('last_donation_date') or None)
            messages.success(request, 'Thank you. Your donor profile has been registered.')
            return redirect('patient:donor_register')
    return render(request, 'patient/donor_register.html', {'active_page': 'donor'})


def verify(request):
    if request.method == 'POST':
        name, password = request.POST.get('username', '').strip(), request.POST.get('password', '')
        try:
            patient = Patient.objects.get(name__iexact=name)
        except Patient.DoesNotExist:
            messages.error(request, 'No account was found with that name.')
        else:
            if check_password(password, patient.password):
                request.session['patient_id'] = patient.id
                return redirect('patient:home')
            messages.error(request, 'Incorrect password. Please try again.')
    return redirect('patient:login')
