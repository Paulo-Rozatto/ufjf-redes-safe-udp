import socket
import struct
import random
from package import Package, TYPE
from constants import *

# random.seed(42)
random.seed(123213)

# Criar um datagrama de socket
udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Atribuindo o endereço e a porta ao socket
udp_socket.bind((SERVER_ADDRESS, SERVER_PORT))

file = []
window_size = DEFAULT_WINDOW_SIZE
window = [None] * window_size
start, end = 0, 0

def send_package(package):
    msgEncoded = package.encode()
    # Embala o pacote propio dentro de um pacote udp
    udp_header = struct.pack(
        "!IIII", SERVER_PORT, SERVER_PORT, len(msgEncoded), package.checksum()
    )
    udp_packet = udp_header + msgEncoded
    udp_socket.sendto(udp_packet, address)

def nextStart(array):
    for i in range(1, len(array)):
        if array[i] == None:
            return start + i
    return start + window_size

print("UDP server up and listening")
while True:
    try:
        udp_socket.settimeout(TIME_OUT_SERVER)
        udp_packet, address = udp_socket.recvfrom(PACKAGE_SIZE)
        udp_header = struct.unpack("!IIII", udp_packet[:16])
        udp_data = udp_packet[16:]
        correct_checksum = udp_header[3]
        package = Package(bytes=udp_data)
        isError = random.random() < ERROR_RATE

        if correct_checksum != package.checksum() or isError:  # send nak
            # print("Checksum error")
            # print("Corrupted message: {}".format(package))
            window_size = max(int(window_size / 2), 1)
            package = Package(TYPE["NAK"], 0, start, window_size)
            # print("Sending NAK {}".format(package.ack_number))
            send_package(package)
            continue

        # print("Received message: {}".format(package))

        if package.type == TYPE["FIN"]:
            # print("Closing connection")
            print("File: {}".format([str(x.data) for x in file]))
            package = Package(TYPE["FIN"], 0, 0, 0, "")
            send_package(package)
            break

        if package.seq_number == start:
            # print("Added package to file")
            new_start = nextStart(window)
            file.append(package)
            for i in range(start + 1, new_start):
                file.append(window[i - start])
            start = new_start
            window_size = min(window_size + 1, MAX_WINDOW_SIZE)
            window = [None] * window_size
            package = Package(TYPE["ACK"], 0, start, window_size)
            print("Sending ACK {}".format(package.ack_number))
            send_package(package)
        elif None not in window[1:]:
            print("Window is full")
            window_size = max(window_size / 2, 1)
            package = Package(TYPE["NAK"], 0, start, window_size)
            send_package(package)
            continue
        elif package.seq_number > start and package.seq_number < start + window_size:
            # print("Added package to buffer, send nack for package {}".format(start))
            window[package.seq_number - start] = package
            package = Package(TYPE["NAK"], 0, start, window_size)
            send_package(package)
    except socket.timeout:
        print("Timeout")
        break
