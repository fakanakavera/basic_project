from django.urls import path
from .views.views import CarTelemetryLapView
from .views.basic_data import unique_sessionUIDs, test_api, get_track_from_sessionUID

urlpatterns = [
    path('test/', test_api, name='test'),
    path('get-track-from-sessionUID/<int:sessionUID>/', get_track_from_sessionUID, name='get-track-from-sessionUID'),
    path('unique-sessionUIDs/', unique_sessionUIDs, name='unique-sessionUIDs'),
    path('car-telemetry/lap/<int:lap_number>/', CarTelemetryLapView.as_view(), name='car-telemetry-by-lap'),
]
