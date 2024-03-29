from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns =[
    path("auth/", obtain_auth_token),
    path("auth/parking/", views.parking_app_auth),
    path("download-csv/", views.CSVDownloadView.as_view()),

    path("covered_parking/areas/", views.CoveredParkingAreaListAPIView.as_view()),
    path("covered_parking/", views.CoveredParkingAPIView.as_view()),
    path("sse/covered_parking_status/", views.CoveredParkingSSEView),

    path("parking/status/", views.ParkingStatusAPIView.as_view()),
    path("parking/manual/create/", views.ManualParkingEntryCreateAPIView.as_view()),
]