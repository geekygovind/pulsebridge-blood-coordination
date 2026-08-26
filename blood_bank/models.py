from django.db import models
from hospital.models import BloodRequest
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


UNIT_STATUS_CHOICES = [
    ('AVAILABLE', 'Available'),
    ('RESERVED', 'Reserved'),
    ('USED', 'Used'),
    ('EXPIRED', 'Expired'),
]



class BloodBank(models.Model):
    name = models.CharField(max_length=200)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name
    

class BloodTransfer(models.Model):
    request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE)
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    units_provided = models.PositiveIntegerField()
    transfer_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer for Request {self.request.id}"



class BloodUnit(models.Model):
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    component_type = models.CharField(max_length=3, choices=COMPONENT_CHOICES)
    units = models.PositiveIntegerField()
    donation_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, choices=UNIT_STATUS_CHOICES, default='AVAILABLE')

    def __str__(self):
        return f"{self.blood_group} - {self.component_type} ({self.units})"
