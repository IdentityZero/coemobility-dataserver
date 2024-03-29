from django.db.models import Prefetch, Avg, Min
from django.db.models.functions import ExtractHour, ExtractMinute, ExtractSecond, TruncDate

from django.http import JsonResponse,StreamingHttpResponse, HttpResponse
from datetime import datetime
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser



import asyncio
import csv
import time
import random

# Models
from django.contrib.auth.models import User
from Parking.models import ParkingSettings,Parking,ManualEntryParking
from Vehicles.models import VehicleCategory, Vehicles, VehicleRFID
from Users.models import Identity

from .serializers import ParkingDataSerializer

from django_eventstream import send_event

def parkingStatus(request):
    #!TODO on deployment, objects.all for parking and manual parking to current date only
    date_now = datetime.now()
    data = {}
    parking_data = {}

    roles = Identity.objects.all()
    vehicle_categories = VehicleCategory.objects.all()
    parking_settings = ParkingSettings.objects.all()

    parking = Parking.objects.filter(time_out__isnull=True)
    manual_entries = ManualEntryParking.objects.all()

    for role in roles:
        parking_data[str(role)] = {}
        role_name = role.identity_name
        role_filter = parking.filter(vehicle_rfid__vehicle__vehicle_owner__profile__user_identity=role.id)
        manual_role_filter = manual_entries.filter(identity=role.id)

        for vehicle_category in vehicle_categories:
            vehicle_category_name = vehicle_category.vehicle_category

            # Get max parking per role and category set
            settings_keyword = f"MAX_{role_name.upper()}_{vehicle_category_name.upper()}"
            try:
                max_per_role_and_category = int(parking_settings.get(keyword=settings_keyword).value)
                error = "No errors"
            except ParkingSettings.DoesNotExist:
                max_per_role_and_category = 999
                error = f"{settings_keyword} is not yet set"
            
            # Parking by rfid
            category_filter = role_filter.filter(vehicle_rfid__vehicle__vehicle_classification__vehicle_category=vehicle_category.id).count()

            # Parking by manual entry
            manual_category_filter = manual_role_filter.filter(vehicle_category=vehicle_category.id)
            entrance = manual_category_filter.filter(action="entry").count()
            exit = manual_category_filter.filter(action="exit").count()

            active_manual_parking = entrance - exit

            occupants = category_filter + active_manual_parking

            parking_data[str(role)][str(vehicle_category)] = {
                "max":max_per_role_and_category,
                "occupied":occupants,
                "available": max_per_role_and_category - occupants,
                "date": date_now,
                "error": error,
            }

    data['roles'] = [role.identity_name for role in roles]
    data['vehicle_categories'] = [vehicle_category.vehicle_category for vehicle_category in vehicle_categories]
    data['parking_data'] = parking_data

    return JsonResponse(data)

def retrieveUsersLatestParkingRecord(request, id):
    data = {'username': id}

    user = User.objects.get(id=id)

    vehicles = Vehicles.objects.filter(vehicle_owner=user)
    if not vehicles.exists():
        data['vehicle'] = None
        return JsonResponse(data)

    data['vehicle'] = []
    for vehicle in vehicles:
        rfid = VehicleRFID.objects.filter(vehicle=vehicle)
        vehicle_data = {
            "plate_number": vehicle.vehicle_plate_number,
        }

        if not rfid.exists():
            vehicle_data["rfid"] = False
        else:
            vehicle_data["rfid"] = True
            
            latest = Parking.objects.filter(vehicle_rfid=rfid.first()).last()
            try:

                vehicle_data["latest_record"] = {
                    "entry": latest.time_in,
                    "exit": latest.time_out,
                }
            except AttributeError:
                # Has no entry yet
                vehicle_data["latest_record"] = {
                    "entry": None,
                    "exit": None,
                }

        data["vehicle"].append(vehicle_data)

    return JsonResponse(data)

def retrieveAllParkingRecord(request, id):
    user = User.objects.get(pk=id)
    vehicles = Vehicles.objects.filter(vehicle_owner=user).prefetch_related('vehiclerfid_set')
    
    rfids = VehicleRFID.objects.filter(vehicle__in=vehicles)
    parkings = Parking.objects.filter(vehicle_rfid__in=rfids).order_by('-time_in')
    
    serializer = ParkingDataSerializer(parkings, many=True)
    serialized_data =JSONRenderer().render(serializer.data).decode('utf-8')
    
    data = {
        "total": parkings.count(),
        "parking_data": serialized_data
    }

    return JsonResponse(data)



def computeAverageTime(datetimes):
    total_hours = sum(dt.hour for dt in datetimes)
    total_minutes = sum(dt.minute for dt in datetimes)
    total_seconds = sum(dt.second for dt in datetimes)

    # Calculate the average time components
    avg_hours = total_hours // len(datetimes)
    avg_minutes = total_minutes // len(datetimes)
    avg_seconds = total_seconds // len(datetimes)

    # Create the average datetime object
    avg_time = datetime(1900, 1, 1, avg_hours, avg_minutes, avg_seconds)

    return avg_time

timeFormat = "%I:%M:%S %p"
dateFormat = "%a %b %d, %Y"

def downloadParkingRecords(request, id):
    user = User.objects.get(pk=id)
    vehicles = Vehicles.objects.filter(vehicle_owner=user).prefetch_related('vehiclerfid_set')
    
    rfids = VehicleRFID.objects.filter(vehicle__in=vehicles)
    parkings = Parking.objects.filter(vehicle_rfid__in=rfids).order_by('-time_in')

    first_entries = parkings.annotate(
        date=TruncDate('time_in')
    ).values('date').annotate(
        first_instance=Min('time_in')
    ).order_by('date')

    first_entries_time_in = [d["first_instance"] for d in first_entries if "first_instance" in d]
    averageFirstTimeIn = computeAverageTime(first_entries_time_in).time()
    forCalc_averageFirstTimeIn = datetime.combine(datetime.today(), averageFirstTimeIn)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user.username}_records.csv"'

    writer = csv.writer(response)
    writer.writerow(['Vehicle Plate Number', 'Time in (DATE)', 'Time in (TIME)',f'vs AVG({averageFirstTimeIn})','Time out (DATE)', 'Time out (TIME)'])

    for i,parking in enumerate(parkings):
        time_difference = forCalc_averageFirstTimeIn - parking.time_in
        time_difference = time_difference.total_seconds() // 60

        try:
            try:
                if parking.time_in.date() == parkings[i+1].time_in.date():
                    writer.writerow([parking.vehicle_rfid.vehicle.vehicle_plate_number,
                                    parking.time_in.date().strftime(dateFormat),
                                    parking.time_in.time().strftime(timeFormat),
                                    '',
                                    parking.time_out.date().strftime(dateFormat),
                                    parking.time_out.time().strftime(timeFormat)])
                else:
                    # It is the first instance of the day
                    writer.writerow([parking.vehicle_rfid.vehicle.vehicle_plate_number,
                                    parking.time_in.date().strftime(dateFormat),
                                    parking.time_in.time().strftime(timeFormat),
                                    f'{time_difference} mins',
                                    parking.time_out.date().strftime(dateFormat),
                                    parking.time_out.time().strftime(timeFormat)])
            except IndexError:
                # No more to compare to
                writer.writerow([parking.vehicle_rfid.vehicle.vehicle_plate_number,
                                    parking.time_in.date().strftime(dateFormat),
                                    parking.time_in.time().strftime(timeFormat),
                                    f'{time_difference} mins',
                                    parking.time_out.date().strftime(dateFormat),
                                    parking.time_out.time().strftime(timeFormat)])
            
        except AttributeError:
            # No time out yet
            writer.writerow([parking.vehicle_rfid.vehicle.vehicle_plate_number,
                            parking.time_in.date().strftime(dateFormat),
                            parking.time_in.time().strftime(timeFormat),
                            f'{time_difference} mins'])

    return response
