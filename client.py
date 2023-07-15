import socket
import struct
from package import Package
from constants import *

msgClient = "Hello UDP Server"
msgEncoded = str.encode(msgClient)

# Criando um socket UDP do lado do cliente
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Enviar para o servidor usando o socket UDP criado
UDPClientSocket.sendto(msgEncoded, (SERVER_ADDRESS, SERVER_PORT))

udp_packet, sender_address = UDPClientSocket.recvfrom(BUFFER_SIZE)
udp_header = struct.unpack("!IIII", udp_packet[:16])
# os dados do pacote udp eh o pacote do nosso protocolo
udp_data = udp_packet[16:]

correct_checksum = udp_header[3]
packge = Package(bytes=udp_data)

msg = "Server message: {}\n".format(packge)
msg += "Valid checksum: {}\n".format(correct_checksum == packge.checksum())

print(msg)
