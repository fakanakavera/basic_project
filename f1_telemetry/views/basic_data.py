from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Header

@api_view(['GET'])
def unique_sessionUIDs(request):
    """
    Retrieve unique sessionUIDs from the Headers data.
    """
    # Fetch unique sessionUIDs from the CarTelemetry data
    unique_sessionUIDs = Header.objects.values_list('sessionUID', flat=True).distinct()
    unique_sessionUIDs = list(unique_sessionUIDs)
    print(f"unique_sessionUIDs: {unique_sessionUIDs}\n")    
    return Response(unique_sessionUIDs)