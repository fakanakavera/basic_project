from rest_framework.decorators import api_view
from rest_framework.response import Response
from .funcs import unique_sessionUIDs, get_trackid_from_sessionUID, get_all_headers_from_sessionUID, get_all_telemetry_from_sessionUID

@api_view(['GET'])
def unique_sessionUIDs(request):
    return Response(unique_sessionUIDs())

@api_view(['GET'])
def get_trackid_from_sessionUID(request, sessionUID):
    return Response(list(get_trackid_from_sessionUID(sessionUID)))

@api_view(['GET'])
def get_all_headers_from_sessionUID(request, sessionUID):
    return Response(get_all_headers_from_sessionUID(sessionUID))

@api_view(['GET'])
def get_all_telemetry_from_sessionUID(request, sessionUID):
    return Response(get_all_telemetry_from_sessionUID(sessionUID))