
import socket
import struct
from package import Package, TYPE
from constants import *

seq_num = 10000
ack_num = 12345
package = Package(TYPE["DATA"], seq_num, ack_num, "Hello UDP Client")
msgEncoded = package.encode()

# Criar um datagrama de socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Atribuindo o endereço e a porta ao socket
UDPServerSocket.bind((SERVER_ADDRESS, SERVER_PORT))

print("UDP server up and listening")
while(True):
    message, address = UDPServerSocket.recvfrom(BUFFER_SIZE)

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

    # Embala o pacote propio dentro de um pacote udp
    udp_header = struct.pack("!IIII", SERVER_PORT, address[1], len(msgEncoded), package.checksum())
    udp_package = udp_header + msgEncoded

    UDPServerSocket.sendto(udp_package, address)