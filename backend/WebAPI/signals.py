from django.dispatch import receiver
from django.db.models.signals import post_save

from Parking.models import Parking, ManualEntryParking, CoveredParking

from django_eventstream import send_event 

@receiver(post_save, sender=ManualEntryParking)
def trial(sender, instance, created, **kwargs):
    # Unpack sender
    vehicle_category = str(instance.vehicle_category)
    identity = str(instance.identity)
    action = str(instance.action)
    crossing_time = instance.crossing_time

    # Send updates to clients connected to eventstream
    send_event("parking_status",
            "message",
            {"topic": "parking",
            "data": {
                "role": identity,
                "vehicle_category": vehicle_category,
                "action": action,
                "date":crossing_time,
            }})
    
    print("Sending event")