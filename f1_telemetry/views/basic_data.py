from rest_framework.decorators import api_view
from rest_framework.response import Response
from .funcs import _unique_sessionUIDs, _get_trackid_from_sessionUID, _get_all_headers_from_sessionUID, _test_api

@api_view(['GET'])
def unique_sessionUIDs(request):
    return Response(_unique_sessionUIDs())

@api_view(['GET'])
def get_trackid_from_sessionUID(request, sessionUID):
    return Response(list(_get_trackid_from_sessionUID(sessionUID)))

@api_view(['GET'])
def get_all_headers_from_sessionUID(request, sessionUID):
    return Response(_get_all_headers_from_sessionUID(sessionUID))

@api_view(['GET'])
def get_all_telemetry_from_sessionUID(request, sessionUID):
    # return Response(_get_all_telemetry_from_sessionUID(sessionUID))
    return Response([])

@api_view(['GET'])
def test_api(request, sessionUID:int, lap_num:int):
    return Response(_test_api(sessionUID, lap_num))