from django.shortcuts import render
from django.http import HttpResponse

from Vehicles.models import VehicleRFID
from Vehicles.serializers import RfidParkingInformationSerializer

# Create your views here.
def home(request):
    try: 
        rfid = VehicleRFID.objects.get(vehicle_rfid="1")
        print(rfid.vehicle.vehicle_image)
        print(rfid.vehicle.vehicle_owner.profile.user_image)
        print(rfid.vehicle.vehicle_owner.profile.user_identity)
        print(rfid.vehicle.vehicle_plate_number)
        print(rfid.vehicle.vehicle_owner.first_name)
        print(rfid.vehicle.vehicle_owner.last_name)
    except VehicleRFID.DoesNotExist:
        pass
    return HttpResponse(f'sdf') 