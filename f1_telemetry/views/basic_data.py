from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Header, PacketSession

@api_view(['GET'])
def unique_sessionUIDs(request):
    """
    Retrieve unique sessionUIDs from the Headers data.
    """
    print('unique_sessionUIDs')
    # Fetch unique sessionUIDs from the CarTelemetry data
    unique_sessionUIDs = Header.objects.values_list('sessionUID', flat=True).distinct()
    unique_sessionUIDs = list(unique_sessionUIDs)
    sessionUID_to_trackid_map = {}
    for sessionUID in unique_sessionUIDs:
        trackids = PacketSession.objects.filter(header__sessionUID=sessionUID).values_list('trackId', flat=True)
        sessionUID_to_trackid_map[sessionUID] = list(trackids)
    print(sessionUID_to_trackid_map)
    return Response([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    # return Response(sessionUID_to_trackid_map)

@api_view(['GET'])
def test_api(request):
    """
    Test API endpoint.
    """
    print('test_api')
    return Response([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])