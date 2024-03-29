from rest_framework import serializers

from .models import CoveredParkingArea, CoveredParking

class CoveredParkingAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoveredParkingArea
        fields = ['area_name','max_parking', 'area_image']

class CoveredParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model =CoveredParking
        fields = ["area", "id_area", "state", "time"]
