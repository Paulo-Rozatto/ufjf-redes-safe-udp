import socket
import struct
from package import Package, TYPE
from constants import *

WINDOW_SIZE = 2
TIME_OUT = 1

msgClient = "Hello UDP Server"
msgEncoded = str.encode(msgClient)
start, end = 0, 0

file = []
for i in range(0, 5):
    file.append(Package(TYPE["DATA"], i, 0, str(i)))

# Criando um socket UDP do lado do cliente
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while True:
    if end >= len(file):
        print("Closing connection")
        package = Package(TYPE["FIN"], 0, 0, "")
        # Embala o pacote propio dentro de um pacote udp
        udp_header = struct.pack("!IIII", SERVER_PORT, SERVER_PORT, len(package.encode()), package.checksum())
        udp_package = udp_header + package.encode()
        UDPClientSocket.sendto(udp_package, (SERVER_ADDRESS, SERVER_PORT))
        break

    if (end - start) < WINDOW_SIZE:
            package = file[end]
            # Embala o pacote propio dentro de um pacote udp
            udp_header = struct.pack("!IIII", SERVER_PORT, SERVER_PORT, len(package.encode()), package.checksum())
            udp_package = udp_header + package.encode()
            UDPClientSocket.sendto(udp_package, (SERVER_ADDRESS, SERVER_PORT))
            end += 1
    try:
        UDPClientSocket.settimeout(TIME_OUT)
        udp_packet, sender_address = UDPClientSocket.recvfrom(BUFFER_SIZE)
        udp_header = struct.unpack("!IIII", udp_packet[:16])
        # os dados do pacote udp eh o pacote do nosso protocolo
        udp_data = udp_packet[16:]
        correct_checksum = udp_header[3]
        package = Package(bytes=udp_data)
        msg = "Server message: {}\n".format(package)
        msg += "Valid checksum: {}\n".format(correct_checksum == package.checksum())
        print(msg)
        start += 1
    except socket.timeout:
        print("Timeout")
        break
