from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CarTelemetry, Lap
from ..serializers import CarTelemetrySerializer

class CarTelemetryLapView(APIView):
    """
    Retrieve CarTelemetry data for lap number <int:lap_number>.
    """
    # def get(self, request, lap_number, *args, **kwargs):
    #     lap_records = Lap.objects.filter(currentLapNum=lap_number)
    #     header_ids = lap_records.values_list('header_id', flat=True)
    #     car_telemetry_records = CarTelemetry.objects.filter(header_id__in=header_ids)
    #     serializer = CarTelemetrySerializer(car_telemetry_records, many=True)
    #     return Response(serializer.data)
    def get(self, request, lap_number, *args, **kwargs):
        # Fetch lap records matching the lap_number
        lap_records = Lap.objects.filter(currentLapNum=lap_number)
        
        # Prepare a response structure
        response_data = []
        
        for lap in lap_records:
            # Fetch car telemetry records associated with each header (lap)
            car_telemetry_records = CarTelemetry.objects.filter(header=lap.header)
            serializer = CarTelemetrySerializer(car_telemetry_records, many=True)
            
            # Append the serialized telemetry data along with the lap distance to the response
            for record in serializer.data:
                response_data.append({
                    **record,
                    "lapDistance": lap.lapDistance
                })
        
        return Response(response_data)
