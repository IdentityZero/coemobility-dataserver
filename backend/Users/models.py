from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image



# Create your models here.
# ! IMPORTANT
# During migration to mySql, add meta and DB_columns

class Department(models.Model):
    dept_abbr = models.CharField(max_length=10, verbose_name="Department Abbreviation", unique=True)
    dept_name = models.CharField(max_length=50, verbose_name="Department Name")

    def __str__(self):
        return self.dept_abbr
    
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments" 

class Identity(models.Model):
    identity_name = models.CharField(max_length=30, verbose_name="Identity Name", unique=True)

    def __str__(self):
        return self.identity_name
    
    class Meta:
        verbose_name = "Identity"
        verbose_name_plural = "Identities" 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(default=settings.DEFAULT_PROFILE_IMAGE, upload_to="profile_pics")
    user_identity = models.ForeignKey(Identity,on_delete=models.SET_NULL, null=True, verbose_name="Role")
    user_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True,verbose_name="Department")
    user_university_number = models.CharField(max_length=20, verbose_name="Student/Employee Number", null=True, blank=True)
    user_contact_number = models.CharField(max_length=20, verbose_name="Contact Number", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles" 
