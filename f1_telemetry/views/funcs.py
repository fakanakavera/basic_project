from ..models import Header, PacketSession, CarTelemetry


def _unique_sessionUIDs() -> list[int]:
    """
    Retrieve unique sessionUIDs from the Headers data.
    """
    # Fetch unique sessionUIDs from the CarTelemetry data
    unique_sessionUIDs = Header.objects.values_list('sessionUID', flat=True).distinct()
    unique_sessionUIDs = list(map(str, unique_sessionUIDs))
    return unique_sessionUIDs

def _get_trackid_from_sessionUID(sessionUID:int) -> int:
    """
    Retrieve the trackId from the sessionUID.
    """
    trackids = PacketSession.objects.filter(header__sessionUID=sessionUID).values_list('trackId', flat=True).distinct()
    return trackids

def _get_all_headers_from_sessionUID(sessionUID:int) -> list[int]:
    """
    Retrieve all headers from the sessionUID.



    needs work
    """
    # fetach all headers id from the sessionUID
    headerids = Header.objects.filter(
        sessionUID=sessionUID, 
        cartelemetry__lap__currentLapNum=1, 
        cartelemetry__participant__aiControlled=False).values_list('id', flat=True).distinct().order_by('id')
    return list(headerids)

def _get_all_telemetry_from_sessionUID(sessionUID:int) -> list[CarTelemetry]:
    """
    Retrieve all telemetry data from the sessionUID.
    """
    print(type(sessionUID))
    # fetch all telemetry data from the sessionUID
    telemetry_data = CarTelemetry.objects.filter(header__sessionUID=sessionUID).values()
    print(len(telemetry_data))
    return list(telemetry_data)

def _test_api(sessionUID:int, lap_num:int) -> list[int]:
    """
    Retrieve all headers from the sessionUID.



    needs work
    """
    # fetach all headers id from the sessionUID
    headerids = Header.objects.filter(
        sessionUID=sessionUID, 
        packetId=2,
        lap__currentLapNum=lap_num,
        ).values_list('id', flat=True).distinct().order_by('id')
    return list(headerids)