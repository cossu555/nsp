import Clients_Servers.Client_Side.Benevolent_Client as BC
import http.client  # For handling HTTP communication
import socket  # For low-level TCP communication
import json  # For JSON serialization and deserialization, JSON for structured data exchange
import time  # For managing delays in communication
from threading import Thread  # For handling concurrent operations
import Certificate.Verify_CERTIFICATE as VerifyCertificate  # Custom module for certificate verification
import Encryption.AES_Encryption as AES_ENCRYPTION  # Custom module for AES encryption
import Encryption.RSA_Encryption as RSA_ENCRYPTION  # Custom module for RSA encryption

class VMClient(BC.Benevolent_Client):
    pass

    def VM_start(self,ip,port):
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((ip, port))
        print(f"Connected to server at {ip}:{port}")
        self.Client = client_socket

    def VM_CERTIFICATE_Check(self):

        # Prepare the ClientHello message
        Client_Hello = self.prepare_data(
            ["START"],  # Start communication
            ["Data"],  # Placeholder content
            [1],  # Protocol version
            [1],  # Session ID
            ["AES"],  # Chosen encryption algorithm
            ["DH"],  # Key exchange algorithm
            ["HMAC"]  # Message authentication code (MAC) algorithm
        )

        print("Client: Sending: 'Client Hello'")
        self.Client.sendall(Client_Hello)  # Send the ClientHello message

        input("Press Enter to continue (3)")

        # Receive ServerHello
        server_hello = self.Client.recv(1024)  # Read server response
        print("Client: Received: 'Server Hello'\n")



        data_dict = json.loads(server_hello.decode('utf-8'))  # Decode the JSON response
        for key, value in data_dict.items():
            print(f"{key}: {value}")
        self.Algo_chose = data_dict["encryption"]  # Store the chosen encryption algorithm

        input("Press Enter to continue (5)")

        # Receive the server's certificate
        print("Client: Receiving: 'Certificate'")
        certificate = self.Client.recv(1024)

        # Verify the server's certificate
        result = VerifyCertificate.verify_certificate(certificate, "server.crt")
        print(f"Client: Certificate verification: {result}")

        # Extract certificate details
        cert_data = VerifyCertificate.get_cert_details(certificate)
        for key, value in cert_data.items():
            print(f"{key}: {value}")

        self.SERVER_PUBLIC_KEY = cert_data["public_key"]  # Store the server's public key

        input("Press Enter to continue (7)")

        # Receive 'Server Done' message
        server_done = self.Client.recv(1024)
        print(f"Client: Received {server_done}")