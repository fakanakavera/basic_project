from django.urls import path
from .views.basic_data import get_all_headers_from_sessionUID, get_trackid_from_sessionUID, unique_sessionUIDs, get_all_telemetry_from_sessionUID

urlpatterns = [
    path('get-all-headers-from-sessionUID/<int:sessionUID>/', get_all_headers_from_sessionUID, name='get-all-headers-from-sessionUID'),
    path('get-track-from-sessionUID/<int:sessionUID>/', get_trackid_from_sessionUID, name='get-track-from-sessionUID'),
    path('unique-sessionUIDs/', unique_sessionUIDs, name='unique-sessionUIDs'),
    path('car-telemetry/<int:sessionUID>/', get_all_telemetry_from_sessionUID, name='car-telemetry-by-lap-sessionUID'),
]
