import json
import asyncio
from django_eventstream import send_event 

from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

# Internal Dependencies
from .models import Parking,UnregisteredParking
from Vehicles.models import VehicleRFID
from Vehicles.serializers import RfidParkingInformationSerializer

class ParkingConsumer(WebsocketConsumer):
    def connect(self):
        print("Connected")
        self.accept()

    def disconnect(self, close_code): 
        print(close_code)
        self.close() 
    
    def receive(self,text_data):
        """
        text_data will contain RFID and time in a dictionary
        dict = ["RFID" : "rfid value", "Time": str(datetime)]

        Response will contain:
            exist: YES OR NO
            status: ENTRANCE OR EXIT
            data:
                Vehicle Image Filename //
                Owner Image Filename //
                Role // 
                Plate Number //
                Name // 
                Time
                vehicle category //
        """

        response = {}

        # Get data
        text_data_json = json.loads(text_data)
        # print(f"I Received: {text_data_json['RFID']}")
        rfid = text_data_json['RFID']
        datetime = text_data_json['Time']
        datetime_split = datetime.split()

        date = datetime_split[0]
        time = datetime_split[1]

        response["date"] = date
        response["time"] = time

        # Retrieve related Information
        try:
            vehicle_instance = VehicleRFID.objects.get(vehicle_rfid=rfid)
            serializer = RfidParkingInformationSerializer(vehicle_instance)

            response["exist"] = True
            response["data"] = serializer.data

            try:
                # Time out
                qs = Parking.objects.get(vehicle_rfid=vehicle_instance, time_out__isnull=True)
                qs.time_out = datetime
                qs.save()
                response["status"] = "EXIT"

            except Parking.DoesNotExist:
                # Time in
                Parking.objects.create(vehicle_rfid=vehicle_instance,time_in=datetime)
                response["status"] = "ENTRANCE"
            
            send_event("parking_status",
            "message",
            {"topic": "parking",
            "data": {
                "role":serializer.data['vehicle_information']['role'],
                "vehicle_category": serializer.data['vehicle_information']['category'],
                "action": response["status"],
                "date":datetime,
            }})
            print("Sending event")

        except VehicleRFID.DoesNotExist:
            response["exist"] = False

            try:
                # Time out
                qs = UnregisteredParking.objects.get(vehicle_rfid=rfid, time_out__isnull=True)
                qs.time_out = datetime
                qs.save()
                response["status"] = "EXIT"

            except UnregisteredParking.DoesNotExist:
                # Time in
                UnregisteredParking.objects.create(vehicle_rfid=rfid,time_in=datetime)
                response["status"] = "ENTRANCE"
        
        json_reponse = json.dumps(response)

        self.send(json_reponse)
