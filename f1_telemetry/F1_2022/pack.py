import socket
import pickle
import argparse

class UDPCapture:
    def __init__(self, ip_address, port, packet_size=1464):
        self.ip_address = ip_address
        self.port = port
        self.packet_size = packet_size
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((self.ip_address, self.port))

    def capture_packets(self, num_packets, file_path):
        packets = []
        for _ in range(num_packets):
            data, addr = self.udp_socket.recvfrom(self.packet_size)
            packets.append((data, addr))
        
        # Serialize and save the packets to a file
        with open(file_path, 'wb') as file:
            pickle.dump(packets, file)
        
        print(f"Captured and saved {num_packets} packets to {file_path}")

class UDPResender:
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def load_and_resend_packets(self, file_path, target_ip, target_port):
        # Load packets from file
        with open(file_path, 'rb') as file:
            packets = pickle.load(file)
        
        # Resend packets
        for data, _ in packets:
            self.udp_socket.sendto(data, (target_ip, target_port))
        
        print(f"Resent {len(packets)} packets to {target_ip}:{target_port}")

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
