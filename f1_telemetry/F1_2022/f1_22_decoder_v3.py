import socket
from .ArrayStructure import *
from .vars import *
from struct import *
import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basic_project.settings')

# Initialize Django
django.setup()

from ..models import Header, CarMotion, Lap, CarSetup, Participant, CarTelemetry, Log, PacketSession

class f1_22_decoder_v3:
    def __init__(self, *args, **kwargs) -> None:
        self.UDP_IP = "192.168.3.14"  # UDP listen IP-address
        self.UDP_PORT = 20777  # UDP listen port
        self.PACKET_SIZE = 1464    # Amount of bytes in packet

        self.decoder_loop_running = True

        print(kwargs.get('print_numofactivecars', False))
        
        self.clear_screen = kwargs.get('clear_screen', False)
        self.print_header = kwargs.get('print_header', False)
        self.print_carmotion = kwargs.get('print_carmotion', False)
        self.print_packetsession = kwargs.get('print_packetsession', False)
        self.print_lap = kwargs.get('print_lap', False)
        self.print_carsetup = kwargs.get('print_carsetup', False)
        self.print_cartelemetry = kwargs.get('print_cartelemetry', False)
        self.print_numofactivecars = kwargs.get('print_numofactivecars', False)
        self.print_participants = kwargs.get('print_participants', False)

        self.save_all = kwargs.get('save_all', False)
        self.save_header = kwargs.get('save_header', False)
        self.save_carmotion = kwargs.get('save_carmotion', False)
        self.save_packetsession = kwargs.get('save_packetsession', False)
        self.save_lap = kwargs.get('save_lap', False)
        self.save_carsetup = kwargs.get('save_carsetup', False)
        self.save_cartelemetry = kwargs.get('save_cartelemetry', False)
        self.save_participants = kwargs.get('save_participants', False)

        self.header_instance = False
        self.participant = False
        self.total_participants = 0
        # self.sessionUID=-1
        # self.sessionTime=-1
        # self.player_car_index = -1

        self.packet_decoder_map = {
            0: self.decode_packet_0,    # CarMotion
            1: self.decode_packet_1,    # Session
            2: self.decode_packet_2,    # Lap
            3: self.decode_packet_3,    # Event (pass for now)
            4: self.decode_packet_4,    # Participants
            5: self.decode_packet_5,    # CarSetup
            6: self.decode_packet_6,    # CarTelemetry
            7: self.decode_packet_3,    # CarStatus (pass for now)
            8: self.decode_packet_3,    # FinalClassification (pass for now)
            9: self.decode_packet_3,    # LobbyInfo (pass for now)
            10: self.decode_packet_3,   # CarDamage (pass for now)
            11: self.decode_packet_3,   # SessionHistory (pass for now)
            12: self.decode_packet_3,   # LapHistory (pass for now)
            13: self.decode_packet_3,   # CarTelemetryHistory (pass for now)
            14: self.decode_packet_3,   # CarStatusHistory (pass for now)
        }

        self.create_socket()


    def create_socket(self) -> None:
        """ Create UDP socket for F1 2022 telemetry """
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind socket to IP and port
        self.udp.bind((self.UDP_IP, self.UDP_PORT))
        print("F1 Telemetry ready")  # Show we're ready
        print("Listening on " + self.UDP_IP + ":" +
              str(self.UDP_PORT))  # Show IP and port
        
    def log_error(self, message:str, event_type:str, data="") -> None:
        """Logs an error message."""
        if data:
            data = self.format_dict_for_log(data)
        Log.objects.create(event_type=event_type, message=f"{message}\n{data}")

    def format_dict_for_log(self, d:dict) -> dict:
        """
            Formats a dictionary into a string for logging purposes.
            For now it just returns the dictionary without formatting.
        """
        return d

    def make_model_dict(self, data:dict) -> dict:
        """
            Creates the dictionary needed to create the model instance.
            the data received is the data decoded from the packet in 
            the global dictionary for that packet.
        """
        d = {}
        for key, value, type in data:
            d[key[2:]] = value
        return d
    
    def print_packet(self, data: dict, title: str = None) -> None:
        """
            Prints the packet data to the console.
        """
        if self.clear_screen:
            # clear the screen keep in mind this is for windows or linux
            os.system('cls' if os.name == 'nt' else 'clear')

        if title:
            print(f"\n{title}\n")

        for key, value, type in data:
            print(f"{key}: {value}\n")
    
    def decoder_loop(self):
        while self.decoder_loop_running:
            self.index = 0
            self.size = 0
            data, addr = self.udp.recvfrom(self.PACKET_SIZE)
            self.decode_header(data)

    def decode_packet(self, packet_data:dict, data_format:dict) -> dict:
        """
            Decodes the packet data according to the data format.
            it uses the self.index to keep track of the position in the data.
            loop through the data_format and unpack the data according to the format
            and size of the data_types dictionary.

            args:
                packet_data: the packet data
                data_format: the global dictionary for the packet

            returns:
                data_format: the data_format which is now filled with the unpacked data. its global
        """
        for x in range(0, len(data_format)):
            # size of the next field in the packet
            self.size = data_types[data_format[x][2]]['size']
            # format of the next field in the packet
            packet_type = data_types[data_format[x][2]]['format']
            # determine the size of the next field in the packet
            packet_size = packet_data[self.index:self.index+self.size]
            # unpack the next field in the packet and assign it to the data_format
            data_format[x][1] = unpack('<' + packet_type, packet_size)[0]
            # increment the index to the next field in the packet
            self.index += self.size

        return data_format

    def decode_header(self, packet_data:dict) -> None:
        """
            Decodes the header of the packet.
            The header is always the first 24 bytes of the packet.
            The header is then used to determine the packet id and
            call the appropriate decode method for that packet id.

            struct PacketHeader{
                uint16 m_packetFormat;              // 2022
                uint8 m_gameMajorVersion;           // Game major version - "X.00"
                uint8 m_gameMinorVersion;           // Game minor version - "1.XX"
                uint8 m_packetVersion;              // Version of this packet type, all start from 1
                uint8 m_packetId;                   // Identifier for the packet type
                uint64 m_sessionUID;                // Unique identifier for the session
                float m_sessionTime;                // Session timestamp
                uint32 m_frameIdentifier;           // Identifier for the frame the data was retrieved on
                uint8 m_playerCarIndex;             // Index of player's car in the array
                uint8 m_secondaryPlayerCarIndex;    // Index of secondary player's car in the array (splitscreen)
                                                    // 255 if no second player
            };
        """
        global header_data
        header_data = self.decode_packet(packet_data, header_data)

        if self.save_all or self.save_header:
            try:
                header_model_dict = self.make_model_dict(header_data)
                self.header_instance, _ = Header.objects.get_or_create(**header_model_dict)
                self.header_instance.save()
            except Exception as e:
                self.log_error(message=e, event_type="Header", data=header_model_dict)

        if self.print_header:
            self.print_packet(header_data, title="Header")

        # get the packet id from the header
        packet_id = header_data[4][1]
        # get the decode method for the packet id
        decode_method = self.packet_decoder_map.get(packet_id)
        if decode_method:
            decode_method(packet_data)
        else:
            message = f"PacketID doesnt exists on packet_decoder_map. packetid is index 4\n"
            self.log_error(event_type="PacketID", message=message, data=header_data)

    def decode_packet_0(self, packet_data:dict) -> None:
        """
            The header is already decoded so we can start decoding the packet data.
            --- for now we are only decoding one car motion data. ---
            struct PacketMotionData{
                PacketHeader m_header;              // Header
                CarMotionData m_carMotionData[22];  // Data for all cars on track
                                                    // Extra player car ONLY data
                float m_suspensionPosition[4];      // Note: All wheel arrays have the following order:
                float m_suspensionVelocity[4];      // RL, RR, FL, FR
                float m_suspensionAcceleration[4];  // RL, RR, FL, FR
                float m_wheelSpeed[4];              // Speed of each wheel
                float m_wheelSlip[4];               // Slip ratio for each wheel
                float m_localVelocityX;             // Velocity in local space
                float m_localVelocityY;             // Velocity in local space
                float m_localVelocityZ;             // Velocity in local space
                float m_angularVelocityX;           // Angular velocity x-component
                float m_angularVelocityY;           // Angular velocity y-component
                float m_angularVelocityZ;           // Angular velocity z-component
                float m_angularAccelerationX;       // Angular velocity x-component
                float m_angularAccelerationY;       // Angular velocity y-component
                float m_angularAccelerationZ;       // Angular velocity z-component
                float m_frontWheelsAngle;           // Current front wheels angle in radians
                };
        """
        global CarMotionData
        CarMotionData = self.decode_packet(packet_data, CarMotionData)
            
        if self.save_all or self.save_carmotion:
            try:
                carmotion_model_dict = self.make_model_dict(CarMotionData)
                carmotion, _ = CarMotion.objects.get_or_create(header=self.header_instance, **carmotion_model_dict)
                carmotion.save()
            except Exception as e:
                self.log_error(message=e, event_type="CarMotion", data=carmotion_model_dict)
        
        if self.print_carmotion:
            self.print_packet(CarMotionData, title="CarMotion")

    def decode_packet_1(self, packet_data:dict) -> None:
        """ Already decoding everything in the packet."""
        global PacketSessionData
        PacketSessionData = self.decode_packet(packet_data, PacketSessionData)

        if self.save_all or self.save_packetsession:
            try:
                packet_session_model_dict = self.make_model_dict(PacketSessionData)
                packet_session, _ = PacketSession.objects.get_or_create(header=self.header_instance, **packet_session_model_dict)
                packet_session.save()
            except Exception as e:
                self.log_error(message=e, event_type="PacketSession", data=packet_session_model_dict)
        
        if self.print_packetsession:
            self.print_packet(PacketSessionData, title="PacketSession")

    def decode_packet_2(self, packet_data:dict) -> None:
        """
            We are only decoding one lap data for now. 
            --- We need to decode all 22 tracking by the participants. ---
            
            struct PacketLapData{
                PacketHeader m_header;          // Header
                LapData m_lapData[22];          // Lap data for all cars on track
                uint8 m_timeTrialPBCarIdx;      // Index of Personal Best car in time trial (255 if invalid)
                uint8 m_timeTrialRivalCarIdx;   // Index of Rival car in time trial (255 if invalid)
            };

            struct LapData{
                uint32 m_lastLapTimeInMS;               // Last lap time in milliseconds
                uint32 m_currentLapTimeInMS;            // Current time around the lap in milliseconds
                uint16 m_sector1TimeInMS;               // Sector 1 time in milliseconds
                uint16 m_sector2TimeInMS;               // Sector 2 time in milliseconds
                float m_lapDistance;                    // Distance vehicle is around current lap in metres  could
                                                        // be negative if line hasnt been crossed yet
                float m_totalDistance;                  // Total distance travelled in session in metres  could
                                                        // be negative if line hasnt been crossed yet
                float m_safetyCarDelta;                 // Delta in seconds for safety car
                uint8 m_carPosition;                    // Car race position
                uint8 m_currentLapNum;                  // Current lap number
                uint8 m_pitStatus;                      // 0 = none, 1 = pitting, 2 = in pit area
                uint8 m_numPitStops;                    // Number of pit stops taken in this race
                uint8 m_sector;                         // 0 = sector1, 1 = sector2, 2 = sector3
                uint8 m_currentLapInvalid;              // Current lap invalid - 0 = valid, 1 = invalid
                uint8 m_penalties;                      // Accumulated time penalties in seconds to be added
                uint8 m_warnings;                       // Accumulated number of warnings issued
                uint8 m_numUnservedDriveThroughPens;    // Num drive through pens left to serve
                uint8 m_numUnservedStopGoPens;          // Num stop go pens left to serve
                uint8 m_gridPosition;                   // Grid position the vehicle started the race in
                uint8 m_driverStatus;                   // Status of driver - 0 = in garage, 1 = flying lap
                                                        // 2 = in lap, 3 = out lap, 4 = on track
                uint8 m_resultStatus;                   // Result status - 0 = invalid, 1 = inactive, 2 = active
                                                        // 3 = finished, 4 = didnotfinish, 5 = disqualified
                                                        // 6 = not classified, 7 = retired
                uint8 m_pitLaneTimerActive;             // Pit lane timing, 0 = inactive, 1 = active
                uint16 m_pitLaneTimeInLaneInMS;         // If active, the current time spent in the pit lane in ms
                uint16 m_pitStopTimerInMS;              // Time of the actual pit stop in ms
                uint8 m_pitStopShouldServePen;          // Whether the car should serve a penalty at this stop
            };
        """
        global LapData
        LapData = self.decode_packet(packet_data, LapData)
        
        if self.save_all or self.save_lap:
            try:
                lap_model_dict = self.make_model_dict(LapData)
                lap, _ = Lap.objects.get_or_create(header=self.header_instance, **lap_model_dict)
                lap.save()
            except Exception as e:
                self.log_error(message=e, event_type="Lap", data=lap_model_dict)
        
        if self.print_lap:
            self.print_packet(LapData, title="Lap")
        
    def decode_packet_3(self, packet_data:dict) -> None:
        pass
        
    def decode_packet_5(self, packet_data:dict) -> None:
        """
            We are only decoding one car setup data for now.
            --- We need to decode all 22 tracking by the participants. ---

            struct CarSetupData{
                uint8 m_frontWing;                  // Front wing aero
                uint8 m_rearWing;                   // Rear wing aero
                uint8 m_onThrottle;                 // Differential adjustment on throttle (percentage)
                uint8 m_offThrottle;                // Differential adjustment off throttle (percentage)
                float m_frontCamber;                // Front camber angle (suspension geometry)
                float m_rearCamber;                 // Rear camber angle (suspension geometry)
                float m_frontToe;                   // Front toe angle (suspension geometry)
                float m_rearToe;                    // Rear toe angle (suspension geometry)
                uint8 m_frontSuspension;            // Front suspension
                uint8 m_rearSuspension;             // Rear suspension
                uint8 m_frontAntiRollBar;           // Front anti-roll bar
                uint8 m_rearAntiRollBar;            // Front anti-roll bar
                uint8 m_frontSuspensionHeight;      // Front ride height
                uint8 m_rearSuspensionHeight;       // Rear ride height
                uint8 m_brakePressure;              // Brake pressure (percentage)
                uint8 m_brakeBias;                  // Brake bias (percentage)
                float m_rearLeftTyrePressure;       // Rear left tyre pressure (PSI)
                float m_rearRightTyrePressure;      // Rear right tyre pressure (PSI)
                float m_frontLeftTyrePressure;      // Front left tyre pressure (PSI)
                float m_frontRightTyrePressure;     // Front right tyre pressure (PSI)
                uint8 m_ballast;                    // Ballast
                float m_fuelLoad;                   // Fuel load
            };

            struct PacketCarSetupData{
                PacketHeader m_header;              // Header
                CarSetupData m_carSetups[22];
            };
        """
        global CarSetupData
        CarSetupData = self.decode_packet(packet_data, CarSetupData)
        
        if self.save_all or self.save_carsetup:
            try:
                carsetup_model_dict = self.make_model_dict(CarSetupData)
                carsetup, _ = CarSetup.objects.get_or_create(header=self.header_instance, **carsetup_model_dict)
                carsetup.save()
            except Exception as e:
                self.log_error(message=e, event_type="CarSetup", data=carsetup_model_dict)

        if self.print_carsetup:
            self.print_packet(CarSetupData, title="CarSetup")
    
        
    

    

    


    

    

    

    def decode_packet_4(self, data):
        """
            struct ParticipantData{
                uint8 m_aiControlled;   // Whether the vehicle is AI (1) or Human (0) controlled
                uint8 m_driverId;       // Driver id - see appendix, 255 if network human
                uint8 m_networkId;      // Network id unique identifier for network players
                uint8 m_teamId;         // Team id - see appendix
                uint8 m_myTeam;         // My team flag 1 = My Team, 0 = otherwise
                uint8 m_raceNumber;     // Race number of the car
                uint8 m_nationality;    // Nationality of the driver
                char m_name[48];        // Name of participant in UTF-8 format null terminated
                                        // Will be truncated with … (U+2026) if too long
                uint8 m_yourTelemetry;  // The player's UDP setting, 0 = restricted, 1 = public
            };

            struct PacketParticipantsData{
                PacketHeader m_header;      // Header
                uint8 m_numActiveCars;      // Number of active cars in the data should match number of
                    // cars on HUD
                ParticipantData m_participants[22];
            };
        """
        global ParticipantsData
        global NumofActiveCars

        NumofActiveCars = self.decode_packet(data, NumofActiveCars)

        if self.print_numofactivecars:
            self.print_packet(NumofActiveCars, title="NumofActiveCars")

        self.size = data_types[ParticipantsData[0][2]]['size']
        data_type = data_types[ParticipantsData[0][2]]['format']
        packet_size = data[self.index:self.index+self.size]
        ParticipantsData[0][1] = unpack('<' + data_type, packet_size)[0]
        
        self.index += self.size
    
        self.total_participants = ParticipantsData[0][1]
        self.driver_id = []
        for i in range(self.total_participants):
            self.driver_id.append(0)
        for p in range(0, self.total_participants):
            for x in range(1, len(ParticipantsData)):
            
                self.size = data_types[ParticipantsData[x][2]]['size']
                ParticipantsData[x][1] = unpack(
                    '<' + data_types[ParticipantsData[x][2]]['format'], data[self.index:self.index+self.size])[0]

                # if ParticipantsData[x][0] == 'm_aiControlled' and ParticipantsData[x][1] == 0:
                #     self.player_car_index = p

                if ParticipantsData[x][0] == 'm_name':
                    ParticipantsData[x][1] = ParticipantsData[x][1].decode(
                        'utf-8').rstrip('\x00')
                self.index += self.size
            
            if self.save_all or self.save_participants:
                try:
                    participant_model_dict = self.make_model_dict(ParticipantsData)
                    participant, _ = Participant.objects.get_or_create(header=self.header_instance, **participant_model_dict)
                    self.driver_id[p] = participant
                    participant.save()
                except Exception as e:
                    self.log_error(message=e, event_type="Participant", data=participant_model_dict)

    

    def decode_packet_6(self, data):
        # os.system('cls')
        for p in range(0, self.total_participants):
            for x in range(0, len(CarTelemetryData)):
                self.size = data_types[CarTelemetryData[x][2]]['size']
                CarTelemetryData[x][1] = unpack(
                    '<' + data_types[CarTelemetryData[x][2]]['format'], data[self.index:self.index+self.size])[0]

                self.index += self.size

            if self.save_all or self.save_cartelemetry:
                try:
                    car_telemetry_model_dict = self.make_model_dict(CarTelemetryData)
                    car_telemetry, _ = CarTelemetry.objects.get_or_create(header=self.header_instance, driverId=self.driver_id[p], **car_telemetry_model_dict)
                    car_telemetry.save()
                except Exception as e:
                    print(f"P: {p}")
                    print(self.driver_id)
                    print(e)
                    print(CarTelemetryData)
                    print('-------------------------------')
                    self.log_error(message=e, event_type="CarTelemetry", data=car_telemetry_model_dict)
            

    
