
import socket
from package import Package, TYPE, TYPE_CONVERTER

PORT = 20001
ADDRESS = "127.0.0.1"
BUFFER_SIZE = 1024

num = 10000
package = Package(TYPE["DATA"], num, num, "Hello UDP Client")

msgServer = "Hello UDP Client"
# msgEncoded = str.encode(msgServer) + num.to_bytes(4, byteorder='big')
msgEncoded = package.encode()

# Criar um datagrama de socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Atribuindo o endereço e a porta ao socket
UDPServerSocket.bind((ADDRESS, PORT))

print("UDP server up and listening")
while(True):
    message, address = UDPServerSocket.recvfrom(BUFFER_SIZE)

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

    UDPServerSocket.sendto(msgEncoded, address)