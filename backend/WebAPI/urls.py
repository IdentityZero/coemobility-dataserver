from django.urls import path, include
import django_eventstream

from . import views

urlpatterns = [
    path("parking/status/", views.parkingStatus),
    path("parking/status/sse/", include(django_eventstream.urls), {"channels": ["parking_status"]}), # Send event is sent from Parking Consumer

    path("parking/records/<int:id>", views.retrieveUsersLatestParkingRecord),
    path("parking/records/<int:id>/all/", views.retrieveAllParkingRecord),
    path("parking/records/<int:id>/download/", views.downloadParkingRecords),
]