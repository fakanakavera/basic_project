import socket
from .ArrayStructure import *
from .vars import *
from struct import *
import os
import django
import time

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basic_project.settings')

# Initialize Django
django.setup()

from ..models import Header, CarMotion, Lap, CarSetup, Participant, CarTelemetry, Log, PacketSession

class f1_22_decoder:
    def __init__(self):
        self.UDP_IP = "192.168.3.14"  # UDP listen IP-address
        self.UDP_PORT = 20777  # UDP listen port
        self.PACKET_SIZE = 1464    # Amount of bytes in packet

        self.save_all = True
        self.save_header = True
        self.save_carmotion = False
        self.save_packetsession = False
        self.save_lap = False
        self.save_carsetup = False

        self.header_instance = False
        self.participant = False
        self.sessionUID=-1
        self.sessionTime=-1
        self.total_participants = 0
        self.player_car_index = -1
        self.decoder_loop_running = True

        self.packet_decoder_map = {
            0: self.decode_packet_0,
            1: self.decode_packet_1,
            2: self.decode_packet_2,
            4: self.decode_packet_4,
            5: self.decode_packet_5,
            6: self.decode_packet_6,
        }

        # Create UDP Socket
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind socket to IP and port
        self.udp.bind((self.UDP_IP, self.UDP_PORT))
        print("F1 Telemetry ready")  # Show we're ready
        print("Listening on " + self.UDP_IP + ":" +
              str(self.UDP_PORT))  # Show IP and port
        
    def format_dict_for_log(self, d):
        """Formats a dictionary into a string for logging purposes."""
        return ', '.join(f'{key}: {value}' for key, value in d.items())

    def log_error(self, e, event_type, data):
        """Logs an error message."""
        Log.objects.create(event_type=event_type, message=f"{e}\n{self.format_dict_for_log(data)}")
        
    def decode_packet(self, data, data_format):
        for x in range(0, len(data_format)):
            self.size = data_types[data_format[x][2]]['size']
            data_format[x][1] = unpack(
                '<' + data_types[data_format[x][2]]['format'], data[self.index:self.index+self.size])[0]
            
            self.index += self.size
        
        return data_format

    def decode_header(self, data):
        global header_data
        #os.system('cls')
        # for x in range(0, len(header_data)):  # Do for every item in the received array
        #     # Set size based on if it's a byte or float
        #     self.size = data_types[header_data[x][2]]['size']
        #     header_data[x][1] = unpack(
        #         '<' + data_types[header_data[x][2]]['format'], data[self.index:self.index+self.size])[0]

        #     #print(header_data[x][0], ': ', header_data[x][1])
        #     self.index += self.size
        header_data = self.decode_packet(data, header_data)

        if self.save_all or self.save_header:
            try:
                # add a header to the database if it doesn't exist, we need to check both sessionUID and sessionTime

                # self.header_instance, created = Header.objects.get_or_create(
                #     sessionUID=header_data[5][1], sessionTime=header_data[6][1])
                header_model_dict = {
                    'packetFormat': header_data[0][1],
                    'gameMajorVersion': header_data[1][1],
                    'gameMinorVersion': header_data[2][1],
                    'packetVersion': header_data[3][1],
                    'packetId': header_data[4][1],
                    'sessionUID': header_data[5][1],
                    'sessionTime': header_data[6][1],
                    'frameIdentifier': header_data[7][1],
                    'playerCarIndex': header_data[8][1],
                    'secondaryPlayerCarIndex': header_data[9][1]
                }
                self.header_instance, created = Header.objects.get_or_create(**header_model_dict)
                # self.header_instance, created = Header.objects.get_or_create(
                #     packetFormat=header_data[0][1],
                #     gameMajorVersion=header_data[1][1],
                #     gameMinorVersion=header_data[2][1],
                #     packetVersion=header_data[3][1],
                #     packetId=header_data[4][1],
                #     sessionUID=header_data[5][1],
                #     sessionTime=header_data[6][1],
                #     frameIdentifier=header_data[7][1],
                #     playerCarIndex=header_data[8][1],
                #     secondaryPlayerCarIndex=header_data[9][1]
                # )

                self.header_instance.save()
            except Exception as e:
                self.log_error(e, "Header", header_model_dict)

        packet_id = header_data[4][1]
        decode_method = self.packet_decoder_map.get(packet_id)
        if decode_method:
            decode_method(data)
        else:
            self.log_error(event_type="Packet_id", message=f"Unknown packet ID: {packet_id}", data=header_data)

        # if header_data[4][1] == 0:
        #     self.decode_packet_0(data)
        # if header_data[4][1] == 1:
        #     self.decode_packet_1(data)
        # if header_data[4][1] == 2:
        #     self.decode_packet_2(data)
        # if header_data[4][1] == 4:
        #     self.decode_packet_4(data)
        # if header_data[4][1] == 5:
        #     self.decode_packet_5(data)
        # if header_data[4][1] == 6:
        #     self.decode_packet_6(data)

    def decode_packet_0(self, data):
        # os.system('cls')
        for x in range(0, len(CarMotionData)):
            self.size = data_types[CarMotionData[x][2]]['size']
            CarMotionData[x][1] = unpack(
                '<' + data_types[CarMotionData[x][2]]['format'], data[self.index:self.index+self.size])[0]

            # print(CarMotionData[x][0], ': ', CarMotionData[x][1])
            self.index += self.size
            
        if self.save_all or self.save_carmotion:
            try:
                carmotion, _ = CarMotion.objects.get_or_create(header=self.header_instance,
                    gForceLateral=CarMotionData[12][1], 
                    gForceLongitudinal=CarMotionData[13][1], 
                    gForceVertical=CarMotionData[14][1], 
                    yaw=CarMotionData[15][1], 
                    pitch=CarMotionData[16][1], 
                    roll=CarMotionData[17][1])
                carmotion.save()
            except Exception as e:
                Log.objects.create(event_type="Error", message=f" {e}\n{CarMotionData}")


    def decode_packet_1(self, data):
        #os.system('cls')
        for x in range(0, len(PacketSessionData)):
            self.size = data_types[PacketSessionData[x][2]]['size']
            PacketSessionData[x][1] = unpack(
                '<' + data_types[PacketSessionData[x][2]]['format'], data[self.index:self.index+self.size])[0]

            self.index += self.size

        if self.save_all:
            try:
                packet_session, _ = PacketSession.objects.get_or_create(header=self.header_instance,
                    weather=PacketSession[0][1], 
                    trackTemperature=PacketSession[1][1], 
                    airTemperature=PacketSession[2][1], 
                    totalLaps=PacketSession[3][1], 
                    trackLength=PacketSession[4][1], 
                    sessionType=PacketSession[5][1], 
                    trackId=PacketSession[6][1], 
                    formula=PacketSession[7][1], 
                    sessionTimeLeft=PacketSession[8][1], 
                    sessionDuration=PacketSession[9][1], 
                    pitSpeedLimit=PacketSession[10][1], 
                    gamePaused=PacketSession[11][1], 
                    isSpectating=PacketSession[12][1], 
                    spectatorCarIndex=PacketSession[13][1], 
                    sliProNativeSupport=PacketSession[14][1],
                    numMarshalZones=PacketSession[15][1],
                    zoneStart=PacketSession[16][1],
                    zoneFlag=PacketSession[17][1],
                    safetyCarStatus=PacketSession[18][1],
                    networkGame=PacketSession[19][1],
                    numWeatherForecastSamples=PacketSession[20][1],
                    timeOffset=PacketSession[21][1],
                    trackTemperatureChange=PacketSession[22][1],
                    airTemperatureChange=PacketSession[23][1],
                    rainPercentage=PacketSession[24][1],
                    forecastAccuracy=PacketSession[25][1],
                    aiDifficulty=PacketSession[26][1],
                    seasonLinkIdentifier=PacketSession[27][1],
                    weekendLinkIdentifier=PacketSession[28][1],
                    sessionLinkIdentifier=PacketSession[29][1],
                    pitStopWindowIdealLap=PacketSession[30][1],
                    pitStopWindowLatestLap=PacketSession[31][1],
                    pitStopRejoinPosition=PacketSession[32][1],
                    steeringAssist=PacketSession[33][1],
                    brakingAssist=PacketSession[34][1],
                    gearboxAssist=PacketSession[35][1],
                    pitAssist=PacketSession[36][1],
                    pitReleaseAssist=PacketSession[37][1],
                    ERSAssist=PacketSession[38][1],
                    DRSAssist=PacketSession[39][1],
                    dynamicRacingLine=PacketSession[40][1],
                    dynamicRacingLineType=PacketSession[41][1],
                    gameMode=PacketSession[42][1],
                    ruleSet=PacketSession[43][1],
                    timeOfDay=PacketSession[44][1],
                    sessionLength=PacketSession[45][1])
                packet_session.save()
            except Exception as e:
                Log.objects.create(event_type="Error", message=f" {e}\n{PacketSessionData}")

    def decode_packet_2(self, data):
        # os.system('cls')
        for x in range(0, len(LapData)):
            self.size = data_types[LapData[x][2]]['size']
            LapData[x][1] = unpack(
                '<' + data_types[LapData[x][2]]['format'], data[self.index:self.index+self.size])[0]

            # print(LapData[x][0], ': ', LapData[x][1])
            self.index += self.size
        
        if self.save_all or self.save_lap:
            try:
                os.system('cls')
                lap, _ = Lap.objects.get_or_create(header=self.header_instance,
                    lastLapTimeInMS=LapData[0][1], 
                    currentLapTimeInMS=LapData[1][1], 
                    sector1TimeInMS=LapData[2][1], 
                    sector2TimeInMS=LapData[3][1], 
                    lapDistance=LapData[4][1], 
                    totalDistance=LapData[5][1],
                    currentLapNum=LapData[8][1])
                lap.save()
                for x in range(0, len(LapData)):
                    print(LapData[x][0], ': ', LapData[x][1])
            except Exception as e:
                Log.objects.create(event_type="Error", message=f" {e}\n{LapData}")
                print(f" {e}\n{LapData}")

    def decode_packet_4(self, data):
        # os.system('cls')
        self.size = data_types[ParticipantsData[0][2]]['size']
        ParticipantsData[0][1] = unpack(
            '<' + data_types[ParticipantsData[0][2]]['format'], data[self.index:self.index+self.size])[0]
        self.total_participants = ParticipantsData[0][1]
        self.index += self.size

        for p in range(0, ParticipantsData[0][1]):
            # print('\nParticipant: ', p+1, ' of ', ParticipantsData[0][1])
            for x in range(1, len(ParticipantsData)):
                self.size = data_types[ParticipantsData[x][2]]['size']
                ParticipantsData[x][1] = unpack(
                    '<' + data_types[ParticipantsData[x][2]]['format'], data[self.index:self.index+self.size])[0]

                if ParticipantsData[x][0] == 'm_aiControlled' and ParticipantsData[x][1] == 0:
                    self.player_car_index = p

                if ParticipantsData[x][0] == 'm_name':
                    ParticipantsData[x][1] = ParticipantsData[x][1].decode(
                        'utf-8').rstrip('\x00')

                # print(ParticipantsData[x][0], ': ', ParticipantsData[x][1])
                self.index += self.size
            
            if self.save_all and self.player_car_index == p:
                try:
                    self.participant, _ = Participant.objects.get_or_create(
                        aiControlled=ParticipantsData[1][1], 
                        driverId=ParticipantsData[2][1], 
                        teamId=ParticipantsData[4][1])
                    self.participant.save()
                except Exception as e:
                    Log.objects.create(event_type="Error", message=f" {e}\n{ParticipantsData}")

    def decode_packet_5(self, data):
        # os.system('cls')
        for x in range(0, len(CarSetupData)):
            self.size = data_types[CarSetupData[x][2]]['size']
            CarSetupData[x][1] = unpack(
                '<' + data_types[CarSetupData[x][2]]['format'], data[self.index:self.index+self.size])[0]

            # print(CarSetupData[x][0], ': ', CarSetupData[x][1])
            self.index += self.size
        
        if self.save_all or self.save_carsetup:
            try:
                carsetup, _ = CarSetup.objects.get_or_create(header=self.header_instance,
                    frontWing=CarSetupData[0][1], 
                    rearWing=CarSetupData[1][1], 
                    onThrottle=CarSetupData[2][1], 
                    offThrottle=CarSetupData[3][1], 
                    frontCamber=CarSetupData[4][1], 
                    rearCamber=CarSetupData[5][1], 
                    frontToe=CarSetupData[6][1], 
                    rearToe=CarSetupData[7][1], 
                    frontSuspension=CarSetupData[8][1], 
                    rearSuspension=CarSetupData[9][1], 
                    frontAntiRollBar=CarSetupData[10][1], 
                    rearAntiRollBar=CarSetupData[11][1], 
                    frontSuspensionHeight=CarSetupData[12][1], 
                    rearSuspensionHeight=CarSetupData[13][1], 
                    brakePressure=CarSetupData[14][1], 
                    brakeBias=CarSetupData[15][1], 
                    rearLeftTyrePressure=CarSetupData[16][1], 
                    rearRightTyrePressure=CarSetupData[17][1], 
                    frontLeftTyrePressure=CarSetupData[18][1], 
                    frontRightTyrePressure=CarSetupData[19][1], 
                    ballast=CarSetupData[20][1], 
                    fuelLoad=CarSetupData[21][1])
                carsetup.save()
            except Exception as e:
                Log.objects.create(event_type="Error", message=f" {e}\n{CarSetupData}")

    def decode_packet_6(self, data):
        # os.system('cls')
        for p in range(0, self.total_participants):
            for x in range(0, len(CarTelemetryData)):
                self.size = data_types[CarTelemetryData[x][2]]['size']
                CarTelemetryData[x][1] = unpack(
                    '<' + data_types[CarTelemetryData[x][2]]['format'], data[self.index:self.index+self.size])[0]

                #if p == self.player_car_index:
                    #print(CarTelemetryData[x][0], ': ', CarTelemetryData[x][1])

                self.index += self.size

            if self.save_all and self.player_car_index == p:
                try:
                    car_telemetry, _ = CarTelemetry.objects.get_or_create(
                        header=self.header_instance,
                        driverId=self.participant,
                        speed=CarTelemetryData[0][1],
                        throttle=CarTelemetryData[1][1],
                        steer=CarTelemetryData[2][1],
                        brake=CarTelemetryData[3][1],
                        clutch=CarTelemetryData[4][1],
                        gear=CarTelemetryData[5][1],
                        engineRPM=CarTelemetryData[6][1],
                        drs=CarTelemetryData[7][1],
                        revLightsPercent=CarTelemetryData[8][1],
                        revLightsBitValue=CarTelemetryData[9][1],
                        brakesTemperatureRR=CarTelemetryData[10][1],
                        brakesTemperatureRL=CarTelemetryData[11][1],
                        brakesTemperatureFL=CarTelemetryData[12][1],
                        brakesTemperatureFR=CarTelemetryData[13][1],
                        tyresSurfaceTemperatureRR=CarTelemetryData[14][1],
                        tyresSurfaceTemperatureRL=CarTelemetryData[15][1],
                        tyresSurfaceTemperatureFL=CarTelemetryData[16][1],
                        tyresSurfaceTemperatureFR=CarTelemetryData[17][1],
                        tyresInnerTemperatureRR=CarTelemetryData[18][1],
                        tyresInnerTemperatureRL=CarTelemetryData[19][1],
                        tyresInnerTemperatureFL=CarTelemetryData[20][1],
                        tyresInnerTemperatureFR=CarTelemetryData[21][1],
                        engineTemperature=CarTelemetryData[22][1],
                        tyresPressureRR=CarTelemetryData[23][1],
                        tyresPressureRL=CarTelemetryData[24][1],
                        tyresPressureFL=CarTelemetryData[25][1],
                        tyresPressureFR=CarTelemetryData[26][1],
                        surfaceTypeRR=CarTelemetryData[27][1],
                        surfaceTypeRL=CarTelemetryData[28][1],
                        surfaceTypeFL=CarTelemetryData[29][1],
                        surfaceTypeFR=CarTelemetryData[30][1]
                    )

                    car_telemetry.save()
                except Exception as e:
                    Log.objects.create(event_type="Error", message=f" {e}\n{CarTelemetryData}")
            

    def decoder_loop(self):
        while self.decoder_loop_running:
            self.index = 0
            self.size = 0
            data, addr = self.udp.recvfrom(self.PACKET_SIZE)
            self.decode_header(data)
