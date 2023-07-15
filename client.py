
import socket
from package import Package, TYPE

BUFFER_SIZE = 1024

msgClient = "Hello UDP Server"
msgEncoded = str.encode(msgClient)
serverAddressPort = ("127.0.0.1", 20001)

# Criando um socket UDP do lado do cliente
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Enviar para o servidor usando o socket UDP criado
UDPClientSocket.sendto(msgEncoded, serverAddressPort)
 
msgServer = UDPClientSocket.recvfrom(BUFFER_SIZE)
packge = Package(bytes=msgServer[0])
msg = "Message from Server {}".format(packge)

print(msg)