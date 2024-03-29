from django.contrib import admin

from . import models
# Register your models here.
class ParkingColumns(admin.ModelAdmin):
    list_display = ['vehicle_rfid','time_in','time_out']

admin.site.register(models.Parking, ParkingColumns)
admin.site.register(models.UnregisteredParking, ParkingColumns)

class CoveredParkingAreaColumn(admin.ModelAdmin):
    list_display = ['area_name','max_parking', 'area_image']

admin.site.register(models.CoveredParkingArea, CoveredParkingAreaColumn)

class CoveredParkingColumn(admin.ModelAdmin):
    list_display = ['area','id_area', 'state', 'time']

admin.site.register(models.CoveredParking, CoveredParkingColumn)

class ManualEntryParkingColumn(admin.ModelAdmin):
    list_display = ['vehicle_category', 'identity', 'action', 'crossing_time']
    
admin.site.register(models.ManualEntryParking, ManualEntryParkingColumn)

class ParkingSettingsColumn(admin.ModelAdmin):
    list_display = ['keyword', 'value']

admin.site.register(models.ParkingSettings, ParkingSettingsColumn)
