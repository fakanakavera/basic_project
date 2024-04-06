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
            3: self.decode_packet_3,
            4: self.decode_packet_4,
            5: self.decode_packet_5,
            6: self.decode_packet_6,
            7: self.decode_packet_3,
            8: self.decode_packet_3,
            9: self.decode_packet_3,
            10: self.decode_packet_3,
            11: self.decode_packet_3,
            12: self.decode_packet_3,
            13: self.decode_packet_3,
            14: self.decode_packet_3,
        }

        # Create UDP Socket
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind socket to IP and port
        self.udp.bind((self.UDP_IP, self.UDP_PORT))
        print("F1 Telemetry ready")  # Show we're ready
        print("Listening on " + self.UDP_IP + ":" +
              str(self.UDP_PORT))  # Show IP and port
        
    def make_model_dict(self, data):
        d = {}
        for key, value, type in data:
            d[key[2:]] = value
        return d
        
    def format_dict_for_log(self, d):
        """Formats a dictionary into a string for logging purposes."""
        return d
        # return ', '.join(f'{key}: {value} --> {type}' for key, value, type in d)

    def log_error(self, message, event_type, data=""):
        """Logs an error message."""
        if data:
            data = self.format_dict_for_log(data)
        Log.objects.create(event_type=event_type, message=f"{message}\n{data}")
        
    def decode_packet(self, data, data_format):
        for x in range(0, len(data_format)):
            self.size = data_types[data_format[x][2]]['size']
            data_format[x][1] = unpack(
                '<' + data_types[data_format[x][2]]['format'], data[self.index:self.index+self.size])[0]
            
            self.index += self.size
        
        return data_format

    def decode_header(self, data):
        global header_data
        header_data = self.decode_packet(data, header_data)

        if self.save_all or self.save_header:
            try:
                header_model_dict = self.make_model_dict(header_data)
                self.header_instance, _ = Header.objects.get_or_create(**header_model_dict)

                self.header_instance.save()
            except Exception as e:
                self.log_error(message=e, event_type="Header", data=header_model_dict)

        packet_id = header_data[4][1]
        decode_method = self.packet_decoder_map.get(packet_id)
        if decode_method:
            decode_method(data)
        else:
            pass
            # self.log_error(event_type="PacketID", message="PacketID doesnt exists on packet_decoder_map.\n", data=header_data)

    def decode_packet_0(self, data):
        global CarMotionData
        CarMotionData = self.decode_packet(data, CarMotionData)
            
        if self.save_all or self.save_carmotion:
            try:
                carmotion_model_dict = self.make_model_dict(CarMotionData)
                carmotion, _ = CarMotion.objects.get_or_create(header=self.header_instance, **carmotion_model_dict)
                carmotion.save()
            except Exception as e:
                print(CarMotionData)
                self.log_error(message=e, event_type="CarMotion", data=carmotion_model_dict)


    def decode_packet_1(self, data):
        global PacketSessionData
        PacketSessionData = self.decode_packet(data, PacketSessionData)

        if self.save_all:
            try:
                packet_session_model_dict = self.make_model_dict(PacketSessionData)
                packet_session, _ = PacketSession.objects.get_or_create(header=self.header_instance, **packet_session_model_dict)
                packet_session.save()
            except Exception as e:
                self.log_error(message=e, event_type="PacketSession", data=packet_session_model_dict)

    def decode_packet_2(self, data):
        global LapData
        LapData = self.decode_packet(data, LapData)
        
        if self.save_all or self.save_lap:
            try:
                lap_model_dict = self.make_model_dict(LapData)
                lap, _ = Lap.objects.get_or_create(header=self.header_instance, **lap_model_dict)
                lap.save()
            except Exception as e:
                self.log_error(message=e, event_type="Lap", data=lap_model_dict)

    def decode_packet_3(self, data):
        pass

    def decode_packet_4(self, data):
        global ParticipantsData
        ParticipantsData = self.decode_packet(data, ParticipantsData)
        self.total_participants = ParticipantsData[0][1]
        for p in range(0, ParticipantsData[0][1]):
            # print('\nParticipant: ', p+1, ' of ', ParticipantsData[0][1])
            for x in range(1, len(ParticipantsData)):
                self.size = data_types[ParticipantsData[x][2]]['size']
                ParticipantsData[x][1] = unpack(
                    '<' + data_types[ParticipantsData[x][2]]['format'], data[self.index:self.index+self.size])[0]

                print(ParticipantsData[x][0], ': ', ParticipantsData[x][1])
                if ParticipantsData[x][0] == 'm_aiControlled' and ParticipantsData[x][1] == 0:
                    self.player_car_index = p

                if ParticipantsData[x][0] == 'm_name':
                    ParticipantsData[x][1] = ParticipantsData[x][1].decode(
                        'utf-8').rstrip('\x00')

                # print(ParticipantsData[x][0], ': ', ParticipantsData[x][1])
                self.index += self.size
            
            if self.save_all and self.player_car_index == p:
                try:
                    participant_model_dict = self.make_model_dict(ParticipantsData)
                    participant, _ = Participant.objects.get_or_create(header=self.header_instance, **participant_model_dict)
                    participant.save()
                except Exception as e:
                    self.log_error(message=e, event_type="Participant", data=participant_model_dict)

    def decode_packet_5(self, data):
        global CarSetupData
        CarSetupData = self.decode_packet(data, CarSetupData)
        
        if self.save_all or self.save_carsetup:
            try:
                carsetup_model_dict = self.make_model_dict(CarSetupData)
                carsetup, _ = CarSetup.objects.get_or_create(header=self.header_instance, **carsetup_model_dict)
                carsetup.save()
            except Exception as e:
                self.log_error(message=e, event_type="CarSetup", data=carsetup_model_dict)

    def decode_packet_6(self, data):
        # os.system('cls')
        print(f"total part: {self.total_participants}")
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
                    car_telemetry_model_dict = self.make_model_dict(CarTelemetryData)
                    print(car_telemetry_model_dict)
                    car_telemetry, _ = CarTelemetry.objects.get_or_create(header=self.header_instance, **car_telemetry_model_dict)
                    car_telemetry.save()
                except Exception as e:
                    print(e)
                    print(CarTelemetryData)
                    print('-------------------------------')
                    self.log_error(message=e, event_type="CarTelemetry", data=car_telemetry_model_dict)
            

    def decoder_loop(self):
        while self.decoder_loop_running:
            self.index = 0
            self.size = 0
            data, addr = self.udp.recvfrom(self.PACKET_SIZE)
            self.decode_header(data)
