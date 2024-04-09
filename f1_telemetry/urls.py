from django.urls import path
from views.views import CarTelemetryLapView
from views.basic_data import unique_sessionUIDs

urlpatterns = [
    path('unique-sessionUIDs/', unique_sessionUIDs, name='unique-sessionUIDs'),
    path('car-telemetry/lap/<int:lap_number>/', CarTelemetryLapView.as_view(), name='car-telemetry-by-lap'),
]
