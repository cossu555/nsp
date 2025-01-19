from Clients_Servers.Server_Side.Server import Server
from Clients_Servers.Client_Side.Benevolent_Client import Benevolent_Client
import time

HTTP_PORT = 80
HTTPS_PORT= 443
IPS = ""
SERVER_ADDRESS = "127.0.0.1"

Server = Server()
Server.startHTTP(HTTP_PORT, IPS)
time.sleep(0.01)

Benevolent_Client = Benevolent_Client()
Benevolent_Client.http_start(SERVER_ADDRESS, HTTP_PORT)
Benevolent_Client.Send_Message("Hi server\n")
time.sleep(0.1)

print(f"State of the client's connection : {Benevolent_Client.Client}")
print(f"The client disconnetts from: {SERVER_ADDRESS}:{HTTP_PORT}")
Benevolent_Client.http_end()     #il client frees the port 80
print(f"State of the client's connection : {Benevolent_Client.Client}\n")
time.sleep(0.1)

print("Start of HTTPS'protocol :\n")

print("\nStart 3-WAY Handshake :\n")
Server.TCP_handshake(SERVER_ADDRESS, HTTPS_PORT)
time.sleep(0.1)
Benevolent_Client.TCP_handshake(SERVER_ADDRESS, HTTPS_PORT)
time.sleep(0.1)

print("\nStart Certificate Check:\n")
Benevolent_Client.CERTIFICATE_Check()
time.sleep(0.1)
Server.CHERTIFICATE_check()
time.sleep(0.1)

print("\nStart Key Exchange:\n")


Benevolent_Client.key_exchange()
time.sleep(0.1)
Server.key_exchange()

Benevolent_Client.final_exchange()
Server.final_exchange()
time.sleep(0.1)


print("\nSESSION KEYS:\n")

print(f"Client: {Benevolent_Client.SESSION_KEY}")
print(f"Server: {Server.SESSION_KEY}")

print("Message's test:")

Benevolent_Client.send_a_msg(input("Write message to be send: "))
Server.recieve_msg()
