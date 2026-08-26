from datetime import date

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from hospital.models import BloodRequest
from .models import BloodBank, BloodTransfer, BloodUnit


def home(request):
    inventory_count = BloodUnit.objects.filter(status='AVAILABLE', expiry_date__gte=date.today()).aggregate(total=Sum('units'))['total'] or 0
    return render(request, 'blood_bank/home.html', {'active_page': 'home', 'inventory_count': inventory_count})


def availability(request):
    city, blood_group = request.GET.get('city', '').strip(), request.GET.get('blood_group', '').strip()
    inventory = BloodUnit.objects.filter(status='AVAILABLE', expiry_date__gte=date.today())
    if city:
        inventory = inventory.filter(blood_bank__city__iexact=city)
    if blood_group:
        inventory = inventory.filter(blood_group=blood_group)
    results = inventory.values('blood_bank__name', 'blood_bank__city', 'blood_group').annotate(total_units=Sum('units')).order_by('blood_bank__name', 'blood_group')
    cities = BloodBank.objects.exclude(city='').values_list('city', flat=True).distinct().order_by('city')
    return render(request, 'blood_bank/availability.html', {'active_page': 'availability', 'results': results, 'cities': cities, 'selected_city': city, 'selected_blood_group': blood_group, 'searched': bool(city or blood_group)})


def update(request):
    banks = BloodBank.objects.order_by('name')
    if request.method == 'POST':
        try:
            bank = banks.get(pk=request.POST.get('blood_bank'))
            unit = BloodUnit(blood_bank=bank, blood_group=request.POST.get('blood_group'), component_type=request.POST.get('component_type'), units=request.POST.get('units'), donation_date=request.POST.get('donation_date'), expiry_date=request.POST.get('expiry_date'), status=request.POST.get('status'))
            unit.full_clean()
            unit.save()
        except (BloodBank.DoesNotExist, ValueError):
            messages.error(request, 'Please select a valid blood bank and enter valid unit details.')
        except Exception:
            messages.error(request, 'Please correct the inventory details and try again.')
        else:
            messages.success(request, 'Blood inventory was added successfully.')
            return redirect('blood_bank:update')
    return render(request, 'blood_bank/update.html', {'active_page': 'update', 'banks': banks, 'today': date.today().isoformat()})


@staff_member_required
def pending_requests(request):
    requests = BloodRequest.objects.filter(status='PENDING').select_related('hospital').order_by('-urgency', 'request_time')
    return render(request, 'blood_bank/pending_requests.html', {'active_page': 'requests', 'requests': requests, 'banks': BloodBank.objects.order_by('name')})


@staff_member_required
@require_POST
def accept_request(request, request_id):
    bank = get_object_or_404(BloodBank, pk=request.POST.get('blood_bank'))
    with transaction.atomic():
        blood_request = get_object_or_404(BloodRequest.objects.select_for_update(), pk=request_id, status='PENDING')
        units = list(BloodUnit.objects.select_for_update().filter(blood_bank=bank, blood_group=blood_request.blood_group, component_type=blood_request.component_type, status='AVAILABLE', expiry_date__gte=date.today(), units__gt=0).order_by('expiry_date'))
        available = sum(unit.units for unit in units)
        if available < blood_request.units_needed:
            messages.error(request, f'{bank.name} has only {available} matching units available; {blood_request.units_needed} are required.')
            return redirect('blood_bank:pending_requests')
        remaining = blood_request.units_needed
        for unit in units:
            used = min(unit.units, remaining)
            unit.units -= used
            if unit.units == 0:
                unit.status = 'USED'
            unit.save(update_fields=('units', 'status'))
            remaining -= used
            if remaining == 0:
                break
        BloodTransfer.objects.create(request=blood_request, blood_bank=bank, units_provided=blood_request.units_needed)
        blood_request.status = 'FULFILLED'
        blood_request.save(update_fields=('status',))
    messages.success(request, f'Request #{blood_request.id} was accepted by {bank.name} and inventory was updated.')
    return redirect('blood_bank:pending_requests')


def login_view(request):
    return redirect('blood_bank:home')


def register(request):
    return redirect('blood_bank:home')
