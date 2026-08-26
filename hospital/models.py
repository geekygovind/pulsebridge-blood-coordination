from django.db import models

# Create your models here.


BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

COMPONENT_CHOICES = [
    ('RBC', 'Red Blood Cells'),
    ('PLT', 'Platelets'),
    ('PLS', 'Plasma'),
]

REQUEST_STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('FULFILLED', 'Fulfilled'),
    ('CANCELLED', 'Cancelled'),
]

UNIT_STATUS_CHOICES = [
    ('AVAILABLE', 'Available'),
    ('RESERVED', 'Reserved'),
    ('USED', 'Used'),
    ('EXPIRED', 'Expired'),
]

URGENCY_CHOICES = [
    ('NORMAL', 'Normal'),
    ('EMERGENCY', 'Emergency'),
]

REQUESTER_TYPE_CHOICES = [
    ('HOSPITAL', 'Hospital'),
    ('PATIENT', 'Patient'),
]

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    
    def __str__(self):
        return self.name


class BloodRequest(models.Model):
    requester_type = models.CharField(max_length=10, choices=REQUESTER_TYPE_CHOICES)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    # patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    component_type = models.CharField(max_length=3, choices=COMPONENT_CHOICES)
    units_needed = models.PositiveIntegerField()
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='NORMAL')
    request_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.blood_group} ({self.units_needed}) - {self.status}"
