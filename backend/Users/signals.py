# from django.conf import settings
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save, pre_save, pre_delete
# from django.dispatch import receiver

# import csv
# from datetime import datetime
# import os

# from .models import Profile

# # When new user is created, create a profile for that user
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# #################### PROFILE IMAGE RELATED ####################
# # Delete old image of the user
# # Logger for images
# profile_log = open(settings.PROFILE_IMAGE_LOG_FILE, newline='',mode='a')
# profile_log_writer = csv.writer(profile_log)

# @receiver(pre_save, sender=Profile)
# def delete_old_user_image(sender, instance,*args,**kwargs):
#     if not instance.pk:
#         # Newly created
#         return False
    
#     try:
#         old_instance = sender.objects.get(pk=instance.pk)
#     except sender.DoesNotExist:
#         return False
    
#     # Image is empty or default image
#     if not old_instance.user_image or old_instance.user_image == settings.DEFAULT_PROFILE_IMAGE:
#         return False
    
#     new_image = instance.user_image
#     if not old_instance.user_image == new_image:
#         old_image_path = old_instance.user_image.path
#         if os.path.isfile(old_image_path):
#             os.remove(old_image_path)

#             old_image_path_relative = old_instance.user_image
#             time_stamp = datetime.now()

#             profile_log_writer.writerow([time_stamp,"DEL", old_image_path_relative])
#             profile_log.flush()

# @receiver(pre_delete, sender=Profile)
# def delete_deleted_users_user_image(sender, instance, **kwargs):

#     # Image is not empty and not default
#     if not instance.user_image == settings.DEFAULT_PROFILE_IMAGE and instance.user_image:
#         image_path = instance.user_image.path
#         if os.path.isfile(image_path):
#             os.remove(image_path)

#             image_path_relative = instance.user_image
#             time_stamp = datetime.now()

#             profile_log_writer.writerow([time_stamp,"DEL", image_path_relative])
#             profile_log.flush()

# # Add added images to logger
# @receiver(post_save, sender=Profile)
# def add_user_user_image(sender,instance, **kwargs):

#     if not settings.DEFAULT_PROFILE_IMAGE == instance.user_image:
#         time_stamp = datetime.now()
#         profile_log_writer.writerow([time_stamp,"ADD", instance.user_image])
#         profile_log.flush()

# #################### END OF PROFILE IMAGE RELATED ####################
