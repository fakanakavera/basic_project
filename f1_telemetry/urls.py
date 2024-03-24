from django.urls import path
from .views import CarTelemetryLapView

urlpatterns = [
    path('car-telemetry/lap/<int:lap_number>/', CarTelemetryLapView.as_view(), name='car-telemetry-by-lap'),
]
