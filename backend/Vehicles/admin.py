from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.VehicleCategory)

class VehicleClassificationColumn(admin.ModelAdmin):
    list_display = ['vehicle_classification', 'vehicle_category']
admin.site.register(models.VehicleClassification, VehicleClassificationColumn)

class VehiclesColumn(admin.ModelAdmin):
    list_display = ['vehicle_owner', 'vehicle_plate_number', 'vehicle_classification']
admin.site.register(models.Vehicles, VehiclesColumn)

class VehicleRFIDColumn(admin.ModelAdmin):
    list_display = ['vehicle', 'vehicle_rfid']
admin.site.register(models.VehicleRFID, VehicleRFIDColumn)