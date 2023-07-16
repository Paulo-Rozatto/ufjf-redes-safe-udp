
import socket
import struct
from package import Package, TYPE
from constants import *

# package = Package(TYPE["DATA"], seq_num, ack_num, "Hello UDP Client")
# msgEncoded = package.encode()

# Criar um datagrama de socket
udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Atribuindo o endereço e a porta ao socket
udp_socket.bind((SERVER_ADDRESS, SERVER_PORT))

file = []
window = [None] * WINDOW_SIZE
start, end = 0, 0

def send_package(package):
    msgEncoded = package.encode()
    # Embala o pacote propio dentro de um pacote udp
    udp_header = struct.pack("!IIII", SERVER_PORT, SERVER_PORT, len(msgEncoded), package.checksum())
    udp_packet = udp_header + msgEncoded
    udp_socket.sendto(udp_packet, address)

def nextStart(array):
    for i in range(1, len(array)):
        if (array[i] == None):
            return start + i
    return start + WINDOW_SIZE

print("UDP server up and listening")
while(True):
    udp_packet, address = udp_socket.recvfrom(PACKAGE_SIZE)
    udp_header = struct.unpack("!IIII", udp_packet[:16])
    udp_data = udp_packet[16:]
    correct_checksum = udp_header[3]
    package = Package(bytes=udp_data)

    if (correct_checksum != package.checksum()): # send nak
        print("Checksum error")
        package = Package(TYPE["NAK"], 0, start, "")
        continue

    print("Received message: {}".format(package))

    if (package.type == TYPE["FIN"]):
        print("Closing connection")
        print("File: {}".format([str(x.data) for x in file]))
        break

    if (package.seq_number == start):
        print("Added package to file")
        new_start = nextStart(window)
        file.append(package)
        for i in range(start + 1, new_start):
            file.append(window[i - start])
        start = new_start
        window = [None] * WINDOW_SIZE
        package = Package(TYPE["ACK"], 0, start, "")
        send_package(package)
    elif (None not in window[1:]):
        print("Window is full")
        package = Package(TYPE["NAK"], 0, start, "")
        send_package(package)
        continue
    elif (package.seq_number > start):
        print("Added package to buffer, send nack for package {}".format(start))
        window[package.seq_number - start] = package
        package = Package(TYPE["NAK"], 0, start, "")
        send_package(package)