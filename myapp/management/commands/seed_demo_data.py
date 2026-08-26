from datetime import date, timedelta

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from blood_bank.models import BloodBank, BloodTransfer, BloodUnit
from hospital.models import BloodRequest, Hospital
from myapp.models import Donor, Patient


class Command(BaseCommand):
    help = 'Create idempotent demo data for PulseBridge.'

    def handle(self, *args, **options):
        password = make_password('DemoPass123!')
        patients = []
        for name, area, city, contact in [
            ('Aarav Shah', 'Navrangpura', 'Ahmedabad', '9876501001'),
            ('Diya Patel', 'Alkapuri', 'Vadodara', '9876501002'),
            ('Kabir Mehta', 'Vesu', 'Surat', '9876501003'),
            ('Anaya Joshi', 'Bopal', 'Ahmedabad', '9876501004'),
            ('Vivaan Desai', 'Adajan', 'Surat', '9876501005'),
        ]:
            patient, _ = Patient.objects.get_or_create(name=name, defaults={'area': area, 'city': city, 'contact_no': contact, 'password': password})
            patients.append(patient)

        donor_data = [
            ('Riya Sharma', 'O+', 'Ahmedabad', '9876510001', True), ('Ishaan Patel', 'A+', 'Ahmedabad', '9876510002', True),
            ('Meera Rao', 'B+', 'Vadodara', '9876510003', True), ('Arjun Singh', 'O-', 'Surat', '9876510004', True),
            ('Nisha Verma', 'AB+', 'Rajkot', '9876510005', False), ('Kunal Shah', 'A-', 'Ahmedabad', '9876510006', True),
            ('Pooja Mehta', 'B-', 'Surat', '9876510007', True), ('Dev Joshi', 'O+', 'Vadodara', '9876510008', True),
            ('Sara Khan', 'AB-', 'Ahmedabad', '9876510009', True), ('Rohan Das', 'O+', 'Rajkot', '9876510010', False),
        ]
        for index, (name, group, city, contact, available) in enumerate(donor_data):
            Donor.objects.get_or_create(name=name, defaults={'blood_group': group, 'city': city, 'contact_no': contact, 'is_available': available, 'last_donation_date': date.today() - timedelta(days=100 + index)})

        hospital_data = [
            ('City Hospital', 'Central', 'Ahmedabad', '079-40001001'), ('Sunrise Medical Centre', 'Vesu', 'Surat', '0261-4001002'),
            ('Harmony Hospital', 'Alkapuri', 'Vadodara', '0265-4001003'), ('CarePoint Hospital', 'Kalawad Road', 'Rajkot', '0281-4001004'),
        ]
        hospitals = {}
        for name, area, city, contact in hospital_data:
            hospitals[name], _ = Hospital.objects.get_or_create(name=name, defaults={'area': area, 'city': city, 'contact_no': contact})

        bank_data = [
            ('RedDrop Blood Centre', 'Navrangpura', 'Ahmedabad', '079-51001001'), ('LifeFlow Blood Bank', 'Vesu', 'Surat', '0261-5101002'),
            ('VitalLink Centre', 'Alkapuri', 'Vadodara', '0265-5101003'), ('Sanjeevani Blood Bank', 'Kalawad Road', 'Rajkot', '0281-5101004'),
        ]
        banks = {}
        for name, area, city, contact in bank_data:
            banks[name], _ = BloodBank.objects.get_or_create(name=name, defaults={'area': area, 'city': city, 'contact_no': contact})

        stock_data = [
            ('RedDrop Blood Centre', 'O+', 'RBC', 18), ('RedDrop Blood Centre', 'A+', 'RBC', 14), ('RedDrop Blood Centre', 'O-', 'RBC', 6), ('RedDrop Blood Centre', 'AB+', 'PLS', 9),
            ('LifeFlow Blood Bank', 'B+', 'RBC', 16), ('LifeFlow Blood Bank', 'O+', 'RBC', 20), ('LifeFlow Blood Bank', 'A-', 'PLT', 8), ('LifeFlow Blood Bank', 'AB-', 'PLS', 4),
            ('VitalLink Centre', 'A+', 'RBC', 22), ('VitalLink Centre', 'B-', 'RBC', 7), ('VitalLink Centre', 'O-', 'RBC', 5), ('VitalLink Centre', 'AB+', 'PLT', 10),
            ('Sanjeevani Blood Bank', 'B+', 'RBC', 13), ('Sanjeevani Blood Bank', 'O+', 'PLT', 11), ('Sanjeevani Blood Bank', 'A-', 'RBC', 6), ('Sanjeevani Blood Bank', 'AB-', 'RBC', 3),
        ]
        for bank_name, group, component, units in stock_data:
            BloodUnit.objects.get_or_create(blood_bank=banks[bank_name], blood_group=group, component_type=component, donation_date=date.today() - timedelta(days=8), defaults={'units': units, 'expiry_date': date.today() + timedelta(days=30), 'status': 'AVAILABLE'})

        request_data = [
            ('City Hospital', 'O-', 'RBC', 3, 'EMERGENCY', 'PENDING'), ('Sunrise Medical Centre', 'B+', 'RBC', 2, 'NORMAL', 'PENDING'),
            ('Harmony Hospital', 'A+', 'RBC', 4, 'EMERGENCY', 'PENDING'), ('CarePoint Hospital', 'AB+', 'PLT', 2, 'NORMAL', 'PENDING'),
            ('City Hospital', 'O+', 'RBC', 2, 'NORMAL', 'FULFILLED'), ('Sunrise Medical Centre', 'A-', 'PLT', 1, 'NORMAL', 'FULFILLED'),
        ]
        created_requests = []
        for hospital_name, group, component, units, urgency, status in request_data:
            request, created = BloodRequest.objects.get_or_create(hospital=hospitals[hospital_name], blood_group=group, component_type=component, units_needed=units, urgency=urgency, status=status, defaults={'requester_type': 'HOSPITAL'})
            if created:
                created_requests.append(request)

        for request in BloodRequest.objects.filter(status='FULFILLED'):
            BloodTransfer.objects.get_or_create(request=request, defaults={'blood_bank': banks['RedDrop Blood Centre'], 'units_provided': request.units_needed})

        self.stdout.write(self.style.SUCCESS('Demo data ready: 5 patients, 10 donors, 4 hospitals, 4 blood banks, inventory, and hospital requests.'))
