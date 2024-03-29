from rest_framework import serializers
from Parking.models import Parking

class ParkingDataSerializer(serializers.ModelSerializer):
    vehicle_plate_number = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Parking
        fields= ['vehicle_rfid','vehicle_plate_number', 'time_in', 'time_out']
    
    def get_vehicle_plate_number(self,obj):
        vehicle_plate_number = obj.vehicle_rfid.vehicle.vehicle_plate_number
        return str(vehicle_plate_number)
    
