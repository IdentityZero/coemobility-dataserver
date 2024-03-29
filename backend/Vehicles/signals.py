# from django.conf import settings
# from django.db.models.signals import post_save, pre_save, pre_delete
# from django.dispatch import receiver

# import csv
# from datetime import datetime
# import os

# from .models import Vehicles

# #################### VEHICLE IMAGE RELATED ####################
# vehicle_log = open(settings.VEHICLE_IMAGE_LOG_FILE, newline='',mode='a')
# vehicle_log_writer = csv.writer(vehicle_log)

# @receiver(pre_delete, sender=Vehicles)
# def delete_deleted_vehicles_vehicle_image(sender, instance, **kwargs):

#     # Image is not empty and not default
#     if not instance.vehicle_image == settings.DEFAULT_VEHICLE_IMAGE and instance.vehicle_image:
#         image_path = instance.vehicle_image.path
#         if os.path.isfile(image_path):
#             os.remove(image_path)

#             image_path_relative = instance.vehicle_image
#             time_stamp = datetime.now()

#             vehicle_log_writer.writerow([time_stamp,"DEL", image_path_relative])
#             vehicle_log.flush()

# @receiver(pre_save, sender=Vehicles)
# def delete_old_user_image(sender, instance,*args,**kwargs):
#     if not instance.pk:
#         # Newly created
#         print("Newly Created")
#         return False
    
#     try:
#         old_instance = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         return False
    
#     # Image is empty or default image
#     if not old_instance.vehicle_image or old_instance.vehicle_image == settings.DEFAULT_VEHICLE_IMAGE:
#         return False
    
#     new_image = instance.vehicle_image
#     if not old_instance.vehicle_image == new_image:
#         old_image_path = old_instance.vehicle_image.path
#         if os.path.isfile(old_image_path):
#             os.remove(old_image_path)

#             old_image_path_relative = old_instance.vehicle_image
#             time_stamp = datetime.now()

#             vehicle_log_writer.writerow([time_stamp,"DEL", old_image_path_relative])
#             vehicle_log.flush()

# @receiver(post_save, sender=Vehicles)
# def add_user_user_image(sender,instance, **kwargs):

#     if not settings.DEFAULT_VEHICLE_IMAGE == instance.vehicle_image:
#         time_stamp = datetime.now()

#         vehicle_log_writer.writerow([time_stamp,"ADD", instance.vehicle_image])
#         vehicle_log.flush()

# #################### END OF VEHICLE IMAGE RELATED ####################
