from django.db import models

from Vehicles.models import VehicleRFID, VehicleCategory
from Users.models import Identity

# Create your models here.
class ParkingSettings(models.Model):
    keyword = models.CharField(max_length=128, verbose_name="Setting keyword", unique=True)
    value = models.CharField(max_length=128, verbose_name="Setting value")

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

class Parking(models.Model):
    vehicle_rfid = models.ForeignKey(VehicleRFID, on_delete=models.CASCADE, verbose_name="Vehicle RFID Code")
    time_in = models.DateTimeField(null=True, verbose_name="Time In")
    time_out = models.DateTimeField(null=True, verbose_name="Time Out")

    class Meta:
        verbose_name = "Parking"
        verbose_name_plural = "Parkings" 

class ManualEntryParking(models.Model):
    ACTION_CHOICES = (
        ('entry', "Entry"),
        ('exit', "Exit")
    )

    vehicle_category = models.ForeignKey(VehicleCategory, on_delete=models.CASCADE, verbose_name="Vehicle Category")
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE, verbose_name="Identity")
    action = models.CharField(max_length=5, choices=ACTION_CHOICES, default='entry')
    crossing_time = models.DateTimeField(null=True, verbose_name="Crossing Times")

    class Meta:
        verbose_name = "Manual Entry"
        verbose_name_plural = "Manual Entries" 

class UnregisteredParking(models.Model):
    vehicle_rfid = models.CharField(max_length=32,verbose_name="Unregistered Vehicle RFID Code")
    time_in = models.DateTimeField(null=True, verbose_name="Time In")
    time_out = models.DateTimeField(null=True, verbose_name="Time Out")

    class Meta:
        verbose_name = "Unregistered RFID Parking"
        verbose_name_plural = "Unregistered RFID Parkings" 

class CoveredParkingArea(models.Model):
    area_name = models.CharField(max_length=16, verbose_name="Covered Parking Area", unique=True)
    max_parking = models.PositiveSmallIntegerField()
    area_image = models.ImageField(upload_to="parking_pics", default="parking_pics/parking_area.png")

    def __str__(self):
        return self.area_name

    class Meta:
        verbose_name = "Covered Parking Area"
        verbose_name_plural = "Covered Parking Areas" 

class CoveredParking(models.Model):
    area = models.ForeignKey(CoveredParkingArea, on_delete=models.CASCADE, verbose_name="Covered Parking")
    id_area = models.PositiveSmallIntegerField() # Add validator here to fit in the max parking size
    state = models.BooleanField(default=False)
    time = models.DateTimeField(verbose_name="Time in")

