
import socket
from package import Package, TYPE

PORT = 20001
ADDRESS = "127.0.0.1"
BUFFER_SIZE = 1024

seq_num = 10000
ack_num = 12345
package = Package(TYPE["DATA"], seq_num, ack_num, "Hello UDP Client")
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