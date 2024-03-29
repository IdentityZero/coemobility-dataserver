from rest_framework import serializers

from .models import VehicleRFID, Vehicles


class RfidParkingInformationSerializer((serializers.ModelSerializer)):
    vehicle_information = serializers.SerializerMethodField()

    class Meta:
        model = VehicleRFID
        fields = ['vehicle_rfid',
                  'vehicle_information']
    
    def get_vehicle_information(self,obj):
        owner_image_path = obj.vehicle.vehicle_owner.profile.user_image.url[6:]
        vehicle_image_path = obj.vehicle.vehicle_image.url[6:]

        return {
            "vehicle_image" : vehicle_image_path,
            "vehicle_plate_number": obj.vehicle.vehicle_plate_number,
            "owner_image" : owner_image_path,
            "role": obj.vehicle.vehicle_owner.profile.user_identity.identity_name,
            "name" : f"{obj.vehicle.vehicle_owner.first_name} {obj.vehicle.vehicle_owner.last_name}",
            "category" : obj.vehicle.vehicle_classification.vehicle_category.vehicle_category
        }
    