# Import needed libraries
from Clients_Servers.Server_Side.Server import Server
from Clients_Servers.Client_Side.Benevolent_Client import Benevolent_Client
import time

# Defining the ports for HTTP and HTTPS, and the server address
HTTP_PORT = 80
HTTPS_PORT = int(input("Write the port you want to use as HTTPS' port: "))
IPS = ""  # Empty string for IP address, can be set to specific IP if needed
SERVER_ADDRESS = "127.0.0.1"  # Localhost address

# Create a Server instance and start the HTTP server
Server = Server()
Server.startHTTP(HTTP_PORT, IPS)  # Starts the HTTP server on port 80
time.sleep(0.01)  # Short delay to ensure server is up and running

# Create a Benevolent_Client instance (client)
Benevolent_Client = Benevolent_Client()
Benevolent_Client.http_start(SERVER_ADDRESS, HTTP_PORT)  # Client connects to server on HTTP port 80
Benevolent_Client.Send_Message("Hi server\n")  # Client sends a message to the server
time.sleep(0.1)  # Short delay to simulate communication time

# Print the state of the client's connection and disconnect it from the HTTP server
print(f"State of the client's connection : {Benevolent_Client.Client}")
print(f"The client disconnects from: {SERVER_ADDRESS}:{HTTP_PORT}")
Benevolent_Client.http_end()  # Client closes the HTTP connection, freeing the port 80
print(f"State of the client's connection : {Benevolent_Client.Client}\n")
time.sleep(0.1)  # Short delay before transitioning to HTTPS

# Start HTTPS protocol (initiating the 3-way handshake)
print("Start of HTTPS protocol :\n")

print("\nStart 3-WAY Handshake :\n")
Server.TCP_handshake(SERVER_ADDRESS, HTTPS_PORT)  # Server initiates TCP handshake for HTTPS on port 443
time.sleep(0.1)  # Short delay before client initiates handshake
Benevolent_Client.TCP_handshake(SERVER_ADDRESS, HTTPS_PORT)  # Client initiates TCP handshake for HTTPS
time.sleep(0.1)  # Short delay for the handshake to complete

# Start certificate verification process
print("\nStart Certificate Check:\n")
Benevolent_Client.CERTIFICATE_Check()  # Client sends certificate check request
time.sleep(0.1)  # Wait for server response
Server.CHERTIFICATE_check()  # Server sends certificate to client for verification
time.sleep(0.1)  # Short delay before moving on to the key exchange

# Start key exchange process
print("\nStart Key Exchange:\n")
Benevolent_Client.key_exchange()  # Client generates and sends encrypted key for the session
time.sleep(0.1)  # Wait for server to process key exchange
Server.key_exchange()  # Server decrypts the received key and prepares the session key

# Finalize the handshake and session setup
Benevolent_Client.final_exchange()  # Client sends 'Change Cipher Spec + Finished'
Server.final_exchange()  # Server acknowledges with its own 'Change Cipher Spec + Finished'
time.sleep(0.1)  # Short delay before confirming session keys

# Display the session keys that will be used for secure communication
print("\nSESSION KEYS:\n")
print(f"Client: {Benevolent_Client.SESSION_KEY}")  # Display client's session key
print(f"Server: {Server.SESSION_KEY}")  # Display server's session key

# Test sending and receiving an encrypted message
print("Message's test:")
Benevolent_Client.send_a_msg(input("Write message to be sent: "))  # Client sends an encrypted message to the server
Server.recieve_msg()  # Server receives and decrypts the message.
