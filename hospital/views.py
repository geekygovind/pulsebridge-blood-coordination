from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import redirect, render

from blood_bank.models import BloodUnit
from .models import BloodRequest, Hospital


def dashboard(request):
    requests = BloodRequest.objects.select_related('hospital').order_by('-request_time')
    return render(request, 'hospital/dashboard.html', {
        'active_page': 'dashboard',
        'pending_requests': requests.filter(status='PENDING').count(),
        'emergency_requests': requests.filter(urgency='EMERGENCY', status='PENDING').count(),
        'available_units': BloodUnit.objects.filter(status='AVAILABLE').aggregate(total=Sum('units'))['total'] or 0,
        'recent_requests': requests[:5],
    })


def availability(request):
    city = request.GET.get('city', '').strip()
    blood_group = request.GET.get('blood_group', '').strip()
    inventory = BloodUnit.objects.filter(status='AVAILABLE')
    if city:
        inventory = inventory.filter(blood_bank__city__iexact=city)
    if blood_group:
        inventory = inventory.filter(blood_group=blood_group)
    results = inventory.values('blood_bank__name', 'blood_bank__city', 'blood_group').annotate(total_units=Sum('units')).order_by('blood_bank__name')
    cities = BloodUnit.objects.exclude(blood_bank__city='').values_list('blood_bank__city', flat=True).distinct().order_by('blood_bank__city')
    return render(request, 'hospital/availability.html', {'active_page': 'availability', 'results': results, 'cities': cities, 'selected_city': city, 'selected_blood_group': blood_group, 'searched': bool(city or blood_group)})


def request_blood(request):
    if request.method == 'POST':
        try:
            hospital, _ = Hospital.objects.get_or_create(name='City Hospital', defaults={'area': 'Central', 'city': 'Ahmedabad', 'contact_no': '0000000000'})
            request_record = BloodRequest(
                requester_type='HOSPITAL', hospital=hospital,
                blood_group=request.POST.get('blood_group'),
                component_type=request.POST.get('component_type'),
                units_needed=request.POST.get('units_needed'),
                urgency=request.POST.get('urgency'),
            )
            request_record.full_clean()
            request_record.save()
        except (ValueError, TypeError):
            messages.error(request, 'Please enter valid request details.')
        except Exception:
            messages.error(request, 'Please complete all required fields using valid values.')
        else:
            messages.success(request, f'Request #{request_record.id} was submitted and is awaiting fulfilment.')
            return redirect('hospital:dashboard')
    return render(request, 'hospital/request_blood.html', {'active_page': 'request_blood'})


def about(request):
    return redirect('landing')


def contact(request):
    return redirect('landing')
