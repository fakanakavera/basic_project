import socket
import pickle
import argparse
import time

class UDPResender:
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.PACKET_SIZE = 1464

    def load_and_resend_packets(self, file_path, target_ip, target_port):
        with open(file_path, 'rb') as file:
            packets = pickle.load(file)

        last_send_time = time.time()
        for data, _, delay in packets:
            # Wait for the delay before sending the next packet
            while time.time() < last_send_time + delay:
                time.sleep(0.0001)  # High-resolution sleep
            
            self.udp_socket.sendto(data[:self.PACKET_SIZE], (target_ip, target_port))
            last_send_time = time.time()

        print(f"Resent {len(packets)} packets to {target_ip}:{target_port} with simulated delays")


class UDPResender:
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def load_and_resend_packets(self, file_path, target_ip, target_port):
        # Load packets from file
        with open(file_path, 'rb') as file:
            packets = pickle.load(file)
        
        # Resend packets with the recorded delay
        for data, _, delay in packets:  # Adjusted to unpack delay
            time.sleep(delay)  # Wait for the delay before sending the packet
            self.udp_socket.sendto(data, (target_ip, target_port))
        
        print(f"Resent {len(packets)} packets to {target_ip}:{target_port} with simulated delays")


def main():
    parser = argparse.ArgumentParser(description="UDP Packets Capture and Resend Tool")
    parser.add_argument("--save", nargs=2, metavar=('NUM_PACKETS', 'FILE_NAME'), 
                        help="Capture and save the specified number of UDP packets.")
    parser.add_argument("--send", nargs=1, metavar='FILE_NAME', 
                        help="Load and resend UDP packets from the specified file.")

    args = parser.parse_args()

    if args.save:
        num_packets, file_name = args.save
        udp_capture = UDPCapture("192.168.3.14", 20777)
        udp_capture.capture_packets(int(num_packets), file_name)

    elif args.send:
        file_name = args.send[0]
        udp_resender = UDPResender()
        udp_resender.load_and_resend_packets(file_name, "192.168.3.14", 20777)

if __name__ == "__main__":
    main()
