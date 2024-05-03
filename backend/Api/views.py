from django.conf import settings
from django.db.models import Count, Max
from django.http import HttpResponse, JsonResponse,StreamingHttpResponse
from django.contrib.auth.models import Group
from django_eventstream import send_event

from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

import asyncio
from datetime import datetime
import json
import redis
import time

from Parking.models import CoveredParkingArea, CoveredParking, Parking, ManualEntryParking, ParkingSettings
from Parking.serializers import CoveredParkingAreaSerializer, CoveredParkingSerializer
from Users.models import Identity
from Vehicles.models import VehicleCategory

import asyncio
from django.http import HttpResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render

def parking_app_auth(request):
    # 1. Authenticate the user using the token
    user, token_key = TokenAuthentication().authenticate(request)

    if user is None:
        # Handle unauthenticated request
       return JsonResponse({"Authorized": False})

    # 1 - Guard ID
    if not user.groups.filter(id=1).exists():
        return JsonResponse({"Authorized": False})

    return JsonResponse({"Authorized": True})

class CSVDownloadView(APIView):
    def get(self,request, *args, **kwargs):
        
        body = request.body

        try:
            data = json.loads(body)
            category = data['category']
            if category == "profiles":
                file_path = settings.PROFILE_IMAGE_LOG_FILE
                filename = "profile_pics.csv"
            elif category == "vehicles":
                file_path = settings.VEHICLE_IMAGE_LOG_FILE
                filename = "vehicle_pics.csv"
            else:
                return HttpResponse()

        except:
            print("error")
            return HttpResponse()

        with open(file_path, 'r') as csv_file:
            response = HttpResponse(csv_file.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
    
class CoveredParkingAreaListAPIView(generics.ListAPIView):
    queryset = CoveredParkingArea.objects.all()
    serializer_class = CoveredParkingAreaSerializer

class CoveredParkingAPIView(APIView):
    def get(self,request, *args, **kwargs):
        querysets = CoveredParking.objects.values('area', 'id_area').annotate(latest_time=Max('time')).filter()
        data = []
        for queryset in querysets:
            area = queryset['area']
            id_area = queryset['id_area']
            time = queryset['latest_time']

            qs = CoveredParking.objects.filter(area=area, id_area=id_area, time=time).first()

            qs_area = str(qs.area)
            qs_id_area = int(qs.id_area)
            qs_state = bool(qs.state)
            qs_time = str(qs.time)
            # Append
            to_append = {
                "area": qs_area,
                "id_area": qs_id_area,
                "state": qs_state,
                "time": qs_time,
            }
            data.append(to_append)

        return JsonResponse(data, safe=False)

    def post(self,request):
        data = request.POST
        print(data)

        area = data['area']
        id_area = data['id_area']
        state = data['state']
        current_time = datetime.now()

        area_instance = CoveredParkingArea.objects.filter(area_name=area).first()

        CoveredParking.objects.create(area=area_instance, id_area=id_area, state=state, time=current_time)
    
        return JsonResponse(data, status=status.HTTP_201_CREATED)

class ParkingStatusAPIView(APIView):
    def get(self, request, *args, **kwargs):
        data = {}

        parking = Parking.objects.filter(time_out__isnull=True)

        identities = Identity.objects.all()

        categories = VehicleCategory.objects.all()
        for identity in identities:
            identity_name = identity.identity_name

            filtered_parking_by_identity = parking.filter(vehicle_rfid__vehicle__vehicle_owner__profile__user_identity=identity)
            manual_entries = ManualEntryParking.objects.filter(identity=identity)
            
            for category in categories:
                category_name = category.vehicle_category
                set = f'{identity_name}_{category_name}'
                filtered_parking_by_category = filtered_parking_by_identity.filter(vehicle_rfid__vehicle__vehicle_classification__vehicle_category=category).count()

                manual_entry_by_category = manual_entries.filter(vehicle_category=category)

                manual_entry_by_category_Entering = manual_entry_by_category.filter(action="entry").count()
                manual_entry_by_category_Exiting = manual_entry_by_category.filter(action="exit").count()

                actual_value_of_manual_entry = manual_entry_by_category_Entering - manual_entry_by_category_Exiting


                current_parkers = filtered_parking_by_category + actual_value_of_manual_entry
                data[set] = {
                    "current":current_parkers,
                    "Parking by Manual Entry": actual_value_of_manual_entry,
                    "Parking by RFID": filtered_parking_by_category,
                }

                # Get max from parking settings
                # Format MAX_IDENTITY_VEHICLECATEGORY
                try:
                    settings_keyword = f"MAX_{identity_name.upper()}_{category_name.upper()}"
                    max_per_role_and_category = int(ParkingSettings.objects.get(keyword=settings_keyword).value)
                    data[set]["max"] = max_per_role_and_category
                    data[set]["available"] = max_per_role_and_category-current_parkers
                    
                except ParkingSettings.DoesNotExist:
                    data[set]["Error"] = f"MAX_1{identity_name.upper()}_{category_name.upper()} is not yet set"

        return JsonResponse(data)

class ManualParkingEntryCreateAPIView(APIView):
    def post(self,request):
        
        # time = datetime.now().timestamp()

        # Unpack request data
        role = request.data['role']
        vehicle_category = request.data['vehicle_category']
        action = request.data['action']
        crossing_time = request.data['crossing_time']

        # Get object instance fo role and vehicle category
        role_instance = Identity.objects.get(identity_name=role)
        vehicle_category_instance = VehicleCategory.objects.get(vehicle_category=vehicle_category)

        ManualEntryParking.objects.create(vehicle_category=vehicle_category_instance,
                                          identity=role_instance,
                                          action=action,
                                          crossing_time=crossing_time)

        # time2 = datetime.now().timestamp()
        # print(f"Manual Parking Entry API View took: {time2-time1} seconds")
        return JsonResponse(request.data, status=status.HTTP_201_CREATED)


    def get(self,request):
        # Test again if app is deployed when build in server is not used
        return JsonResponse({"Initialize": "Initialize"})


# Async SSE
async def event_stream():
    redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    while True:
        data = redis_client.rpop('data_queue')

        # Process the data
        if data:
            # print(data)

            yield f'{data}\n\n'

        await asyncio.sleep(1)

async def CoveredParkingSSEView(request):
    """
    Sends server-sent events to the client.
    """
    response = StreamingHttpResponse(event_stream(),content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'
    return response
    # return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    
@receiver(post_save, sender=CoveredParking)
def covered_parking_update(sender, instance, created, **kwargs):

    if created:
        redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

        area = str(instance.area)
        id_area = int(instance.id_area)
        time = str(instance.time)

        if isinstance(instance.state, str):
            state = {"1": True, "0": False}[instance.state]
        else:
            state = bool(instance.state)

        new_parking = {
            "area": area,
            "id_area": id_area,
            "state": state,
            "time": time,
        }

        json_new_parking = json.dumps(new_parking)

        # Push data to the Redis queue
        redis_client.lpush('data_queue', json_new_parking)

        send_event("parking_status",
            "message",
            {"topic": "covered_parking",
            "data": new_parking
            })