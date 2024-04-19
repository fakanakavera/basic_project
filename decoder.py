from f1_telemetry.F1_2022.f1_22_decoder_v3 import f1_22_decoder_v3
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='F1 2022 Telemetry Decoder Options')

    # Defining command-line options
    parser.add_argument('--clear_screen', action='store_true', help='Clear the screen before output')
    parser.add_argument('--print_header', action='store_true', help='Print packet headers')
    parser.add_argument('--print_carmotion', action='store_true', help='Print car motion data')
    parser.add_argument('--print_packetsession', action='store_true', help='Print packet session data')
    parser.add_argument('--print_lap', action='store_true', help='Print lap data')
    parser.add_argument('--print_carsetup', action='store_true', help='Print car setup data')
    parser.add_argument('--print_cartelemetry', action='store_true', help='Print car telemetry data')
    parser.add_argument('--print_numofactivecars', action='store_true', help='Print number of active cars')
    parser.add_argument('--print_participants', action='store_true', help='Print participants data')

    parser.add_argument('--save_all', action='store_true', help='Save all data to file')
    parser.add_argument('--save_header', action='store_true', help='Save packet headers to file')
    parser.add_argument('--save_carmotion', action='store_true', help='Save car motion data to file')
    parser.add_argument('--save_packetsession', action='store_true', help='Save packet session data to file')
    parser.add_argument('--save_lap', action='store_true', help='Save lap data to file')
    parser.add_argument('--save_carsetup', action='store_true', help='Save car setup data to file')
    parser.add_argument('--save_cartelemetry', action='store_true', help='Save car telemetry data to file')
    parser.add_argument('--save_numofactivecars', action='store_true', help='Save number of active cars to file')
    parser.add_argument('--save_participants', action='store_true', help='Save participants data to file')
    # Continue adding parser.add_argument for each option you want to support

    args = parser.parse_args()
    # Create an instance of the decoder
    # Pass the arguments as a dictionary
    decoder = f1_22_decoder_v3(**args.__dict__)
    # Example usage
    decoder.decoder_loop()