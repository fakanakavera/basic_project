from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Header, PacketSession

@api_view(['GET'])
def unique_sessionUIDs(request):
    """
    Retrieve unique sessionUIDs from the Headers data.
    """
    # Fetch unique sessionUIDs from the CarTelemetry data
    unique_sessionUIDs = Header.objects.values_list('sessionUID', flat=True).distinct()
    unique_sessionUIDs = list(unique_sessionUIDs)
    sessionUID_to_trackid_map = {}
    for sessionUID in unique_sessionUIDs:
        trackids = PacketSession.objects.filter(header__sessionUID=sessionUID).values_list('trackId', flat=True).distinct()
        sessionUID_to_trackid_map[str(sessionUID)] = list(trackids)

    return Response(sessionUID_to_trackid_map)

@api_view(['GET'])
def get_track_from_sessionUID(request, sessionUID):
    """
    Retrieve the trackId from the sessionUID.
    """
    trackids = PacketSession.objects.filter(header__sessionUID=sessionUID).values_list('trackId', flat=True).distinct()
    return Response(list(trackids))

@api_view(['GET'])
def get_all_headers_from_sessionUID(request, sessionUID):
    """
    Retrieve all headers from the sessionUID.
    """
    # fetach all headers id from the sessionUID
    headerids = Header.objects.filter(sessionUID=sessionUID).values_list('id', flat=True).distinct().order_by('id')
    return Response(list(headerids))

@api_view(['GET'])
def test_api(request):
    """
    Test API endpoint.
    """
    print('test_api')
    return Response([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])