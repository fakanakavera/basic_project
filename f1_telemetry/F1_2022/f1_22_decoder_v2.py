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

from ..models import Header, CarMotion, Lap, CarSetup, Participant, CarTelemetry

class f1_22_decoder_v2:
    def __init__(self):
        self.UDP_IP = "127.0.0.1"  # UDP listen IP-address
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

        # Create UDP Socket
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind socket to IP and port
        self.udp.bind((self.UDP_IP, self.UDP_PORT))
        print("F1 Telemetry ready")  # Show we're ready
        print("Listening on " + self.UDP_IP + ":" +
              str(self.UDP_PORT))  # Show IP and port

    def decode_header(self, data):
        #os.system('cls')
        for x in range(0, len(header_data)):  # Do for every item in the received array
            # Set size based on if it's a byte or float
            self.size = data_types[header_data[x][2]]['size']
            header_data[x][1] = unpack(
                '<' + data_types[header_data[x][2]]['format'], data[self.index:self.index+self.size])[0]

            #print(header_data[x][0], ': ', header_data[x][1])
            self.index += self.size

        if self.save_all or self.save_header:
            try:
                # add a header to the database if it doesn't exist, we need to check both sessionUID and sessionTime

                self.header_instance, created = Header.objects.get_or_create(
                    sessionUID=header_data[5][1], sessionTime=header_data[6][1])
                self.header_instance.save()
            except Exception as e:
                print(f"Error adding header: {e}")
                print(header_data[6][1])
                time.sleep(1)

        if header_data[4][1] == 0:
            self.decode_packet_0(data)
        if header_data[4][1] == 1:
            self.decode_packet_1(data)
        if header_data[4][1] == 2:
            self.decode_packet_2(data)
        if header_data[4][1] == 4:
            self.decode_packet_4(data)
        if header_data[4][1] == 5:
            self.decode_packet_5(data)
        if header_data[4][1] == 6:
            self.decode_packet_6(data)

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
                print(self.header_instance)
                print(f"Error adding header: {e}")
                time.sleep(1)

    def decode_packet_1(self, data):
        #os.system('cls')
        for x in range(0, len(PacketSessionData)):
            self.size = data_types[PacketSessionData[x][2]]['size']
            PacketSessionData[x][1] = unpack(
                '<' + data_types[PacketSessionData[x][2]]['format'], data[self.index:self.index+self.size])[0]

            self.index += self.size


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
                lap, _ = Lap.objects.get_or_create(header=self.header_instance,
                    lastLapTimeInMS=LapData[0][1], 
                    currentLapTimeInMS=LapData[1][1], 
                    sector1TimeInMS=LapData[2][1], 
                    sector2TimeInMS=LapData[3][1], 
                    lapDistance=LapData[4][1], 
                    totalDistance=LapData[5][1])
                lap.save()
            except Exception as e:
                print(self.header_instance)
                print(f"Error adding header: {e}")
                time.sleep(1)

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
                    print(self.header_instance)
                    print(f"Error adding header: {e}")
                    time.sleep(1)

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
                print(self.header_instance)
                print(f"Error adding header: {e}")
                time.sleep(1)

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
                    print(self.header_instance)
                    print(f"Error adding header: {e}")
                    time.sleep(1)
            

    def decoder_loop(self):
        while self.decoder_loop_running:
            self.index = 0
            self.size = 0
            data, addr = self.udp.recvfrom(self.PACKET_SIZE)
            self.decode_header(data)
