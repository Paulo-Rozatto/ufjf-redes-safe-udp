
import socket
import struct
from package import Package, TYPE
from constants import *

# package = Package(TYPE["DATA"], seq_num, ack_num, "Hello UDP Client")
# msgEncoded = package.encode()

# Criar um datagrama de socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Atribuindo o endereço e a porta ao socket
UDPServerSocket.bind((SERVER_ADDRESS, SERVER_PORT))

file = []
print("UDP server up and listening")
while(True):
    udp_packet, address = UDPServerSocket.recvfrom(BUFFER_SIZE)
    udp_header = struct.unpack("!IIII", udp_packet[:16])
    udp_data = udp_packet[16:]
    correct_checksum = udp_header[3]
    package = Package(bytes=udp_data)

    if (correct_checksum != package.checksum()):
        print("Checksum error")
        continue
    print("Received message: {}".format(package))

    if (package.type == TYPE["FIN"]):
        print("Closing connection")
        break

    if (package.seq_number == len(file)):
        file.append(package)
        print("Added package to file")

    package = Package(TYPE["ACK"], 0, package.seq_number + 1, "")
    msgEncoded = package.encode()
    # Embala o pacote propio dentro de um pacote udp
    udp_header = struct.pack("!IIII", SERVER_PORT, SERVER_PORT, len(msgEncoded), package.checksum())
    udp_packet = udp_header + msgEncoded

    UDPServerSocket.sendto(udp_packet, address)