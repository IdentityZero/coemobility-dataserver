from django.contrib import admin

from . import models

# Register your models here.
class DepartmentColumns(admin.ModelAdmin):
    list_display = ['dept_abbr', 'dept_name']
admin.site.register(models.Department,DepartmentColumns)

class IdentityColumns(admin.ModelAdmin):
    list_display = ['identity_name']
admin.site.register(models.Identity,IdentityColumns)

class ProfileColumn(admin.ModelAdmin):
    list_display = ['username','firstname','lastname','user_identity', 'user_department']

    def username(self, instance):
        return instance.user.username
    
    def firstname(self, instance):
        return instance.user.first_name
    
    def lastname(self, instance):
        return instance.user.last_name
    
admin.site.register(models.Profile, ProfileColumn)
admin.site.site_header = 'Coemobility - Vehicle Identification and Parking Space Monitoring System'
