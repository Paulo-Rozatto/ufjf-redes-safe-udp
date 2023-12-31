import socket
import struct
from package import Package, TYPE
from constants import *

receiverWindow = DEFAULT_WINDOW_SIZE
start, end, ack_count = 0, 0, 0

file = []
chunk_size = 993

def read_file_in_chunks(file_path, chunk_size):
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

print("Reading file...")
for index, chunk in enumerate(read_file_in_chunks(FILE_PATH, chunk_size)):
    package = Package(TYPE["DATA"], index, 0, 0, chunk)
    file.append(package)
print("File read")


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
    if end >= len(file) and ack_count >= len(file):
        print("Sending FIN to close")
        package = Package(TYPE["FIN"], 0, 0, 0, "")
        send_package(package)
        udp_socket.settimeout(TIME_OUT_CLIENT)
        udp_packet, sender_address = udp_socket.recvfrom(PACKAGE_SIZE)
        package = Package(bytes=udp_packet[16:])
        if (package.type == TYPE["FIN"]):
            print("Received FIN {}".format(package))
            break
        continue
    
    while (end - start) < receiverWindow and end < len(file):
        package = file[end]
        print("Sending package {}".format(package.seq_number))
        package.window_size = receiverWindow
        send_package(package)
        end += 1

    try:
        udp_socket.settimeout(TIME_OUT_CLIENT)
        udp_packet, sender_address = udp_socket.recvfrom(PACKAGE_SIZE)
        udp_header = struct.unpack("!IIII", udp_packet[:16])
        udp_data = udp_packet[16:]

        correct_checksum = udp_header[3]
        package = Package(bytes=udp_data)
        msg = "Server message: {}\nValid checksum: {}".format(
            package, correct_checksum == package.checksum()
        )
        print(msg)

        if package.type == TYPE["NAK"] and package.ack_number < len(file):
            print("Received NAK {}".format(package.ack_number))
            receiverWindow = package.window_size
            package = file[package.ack_number]
            send_package(package)
        else:
            print("Received ACK {}".format(package.ack_number))
            start = package.ack_number # max(package.ack_number, end)
            end = start
            receiverWindow = package.window_size
            ack_count = max(ack_count, start)
            print("New start: {}, new end: {}".format(start, end))
    except socket.timeout:
        print("Timeout")
        break
