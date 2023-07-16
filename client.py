import socket
import struct
from package import Package, TYPE
from constants import *

TIME_OUT = 10000

msgClient = "Hello UDP Server"
msgEncoded = str.encode(msgClient)
start, end = 0, 0
receiverWindow = 1

file = []
for i in range(0, 15):
    file.append(Package(TYPE["DATA"], i, 0, receiverWindow, str(i)))

# Criando um socket UDP do lado do cliente
udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def send_package(package):
    msgEncoded = package.encode()
    # Embala o pacote propio dentro de um pacote udp
    udp_header = struct.pack(
        "!IIII", SERVER_PORT, SERVER_PORT, len(msgEncoded), package.checksum()
    )
    udp_packet = udp_header + msgEncoded
    udp_socket.sendto(udp_packet, (SERVER_ADDRESS, SERVER_PORT))


while True:
    if end >= len(file):
        print("Closing connection")
        package = Package(TYPE["FIN"], 0, 0, 0, "")
        send_package(package)
        break

    
    while (end - start) < receiverWindow and end < len(file):
        package = file[end]
        print("Sending package {}".format(package.seq_number))
        package.window_size = receiverWindow
        send_package(package)
        end += 1

    try:
        udp_socket.settimeout(TIME_OUT)
        udp_packet, sender_address = udp_socket.recvfrom(PACKAGE_SIZE)
        udp_header = struct.unpack("!IIII", udp_packet[:16])
        udp_data = udp_packet[16:]

        correct_checksum = udp_header[3]
        package = Package(bytes=udp_data)
        msg = "Server message: {}\nValid checksum: {}".format(
            package, correct_checksum == package.checksum()
        )
        print(msg)

        if package.type == TYPE["NAK"]:
            print("Received NAK {}".format(package.ack_number))
            receiverWindow = package.window_size
            package = file[package.ack_number]
            send_package(package)
        else:
            print("Received ACK {}".format(package.ack_number))
            start = max(package.ack_number, end)
            end = start
            receiverWindow = package.window_size
            print("New start: {}, new end: {}".format(start, end))
    except socket.timeout:
        print("Timeout")
        break
