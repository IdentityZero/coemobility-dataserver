from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from PIL import Image

# Create your models here.
class VehicleCategory(models.Model):
    vehicle_category = models.CharField(max_length=30, verbose_name="Vehicle Category")

    def __str__(self):
        return self.vehicle_category
    
    class Meta:
        verbose_name = "Vehicle Category"
        verbose_name_plural = "Vehicle Categories"

class VehicleClassification(models.Model):
    vehicle_classification = models.CharField(max_length=30, verbose_name="Vehicle Classification")
    vehicle_category = models.ForeignKey(VehicleCategory, on_delete=models.SET_NULL, null=True, verbose_name="Vehicle Category", default=1)

    def __str__(self):
        return self.vehicle_classification
    
    class Meta:
        verbose_name = "Vehicle Classification"
        verbose_name_plural = "Vehicle Classifications"

class Vehicles(models.Model):
    vehicle_owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Vehicle Owner")
    vehicle_image = models.ImageField(default=settings.DEFAULT_VEHICLE_IMAGE, upload_to="vehicle_pics")
    vehicle_plate_number = models.CharField(max_length=10, unique=True,verbose_name="Plate Number")
    vehicle_classification = models.ForeignKey(VehicleClassification, on_delete=models.SET_NULL, null=True, verbose_name="Vehicle Classification", default=1)
    vehicle_model = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles" 

    def __str__(self):
        return f"{self.vehicle_owner.username} - {self.vehicle_plate_number}"

class VehicleRFID(models.Model):
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE, verbose_name="Vehicle")
    vehicle_rfid = models.CharField(max_length=32,unique=True,verbose_name="Vehicle RFID Code")

    def __str__(self):
        return self.vehicle_rfid
    
    class Meta:
        verbose_name = "Vehicle RFID"
        verbose_name_plural = "Vehicle RFIDs" 
