from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Header

def unique_sessionUIDs(request):
    """
    Retrieve unique sessionUIDs from the Headers data.
    """
    # Fetch unique sessionUIDs from the CarTelemetry data
    unique_sessionUIDs = Header.objects.values_list('sessionUID', flat=True).distinct()
    print(f"unique_sessionUIDs: {unique_sessionUIDs}\n")    
    return Response(unique_sessionUIDs)