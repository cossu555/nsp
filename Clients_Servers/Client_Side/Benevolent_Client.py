import http.client  # For handling HTTP communication
import socket  # For low-level TCP communication
import json  # For JSON serialization and deserialization, JSON for structured data exchange
import time  # For managing delays in communication
from threading import Thread  # For handling concurrent operations
import Certificate.Verify_CERTIFICATE as VerifyCertificate  # Custom module for certificate verification
import Encryption.AES_Encryption as AES_ENCRYPTION  # Custom module for AES encryption
import Encryption.RSA_Encryption as RSA_ENCRYPTION  # Custom module for RSA encryption

class Benevolent_Client:

    def __init__(self):
        
        """
        Initialize the client with default values.
        """
        
        self.Client = None  # Placeholder for the client connection
        self.SERVER_PUBLIC_KEY = None  # Server's public key, obtained during the handshake
        self.Algo_chose = None  # Chosen encryption algorithm
        self.SESSION_KEY = None  # Session key for AES encryption

    def http_start(self, server_address, server_port):
        
        """
        Start an HTTP connection to the server.
        :param server_address: The server's IP address or hostname.
        :param server_port: The server's port for HTTP communication.
        """
        
        self.Client = http.client.HTTPConnection(server_address, server_port)  # Create HTTP connection
        print(f"Client connected to {server_address}:{server_port}")  # Inform the user

    def Send_Message(self, message):
        
        """
        Send a message to the server over HTTP.
        :param message: The message to send (string format).
        """
        
        headers = {'Content-Type': 'text/plain'}  # Specify plain text content type
        self.Client.request("POST", "/", body=message, headers=headers)  # Send an HTTP POST request

    def http_end(self):
        
        """
        Close the HTTP connection.
        """
        
        self.Client.close()  # Close the connection
        self.Client = None  # Reset the client

    def TCP_handshake(self, SERVER_ADDRESS, HANDSHAKE_PORT):
        
        """
        Perform a TCP three-way handshake with the server.
        :param SERVER_ADDRESS: The server's IP address or hostname.
        :param HANDSHAKE_PORT: The server's port for the handshake process.
        :return: True if handshake succeeds, False otherwise.
        """
        
        self.Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
        self.Client.connect((SERVER_ADDRESS, HANDSHAKE_PORT))  # Connect to the server

        # Send SYN (synchronize) message
        self.Client.sendall(b"SYN")
        print("Client: Sent: SYN")

        # Receive SYN-ACK (synchronize-acknowledge) message
        syn_ack = self.Client.recv(1024).decode()
        print(f"Client: Received: {syn_ack}")

        if syn_ack == "SYN-ACK":
            # Send ACK (acknowledge) message
            self.Client.sendall(b"ACK")
            print("Client: Sent: ACK")
            return True  # Handshake successful
        else:
            print("Client: Handshake error")
        return False  # Handshake failed

    def prepare_data(self, START_COMM, CONTENT, VERSION, SESSION_ID, ENCRYPTION, KEY_EXCHANGE, MAC):
        
        """
        Prepare JSON data for communication.
        :return: JSON-encoded data as bytes.
        """
        
        data_dict = {
            "start": START_COMM,
            "content": CONTENT,
            "version": VERSION,
            "session": SESSION_ID,
            "encryption": ENCRYPTION,
            "key_exchange": KEY_EXCHANGE,
            "mac": MAC
        }
        data_bytes = json.dumps(data_dict).encode('utf-8')  # Serialize to JSON and encode to bytes
        return data_bytes

    def CERTIFICATE_Check(self):
        
        """
        Start a thread to perform certificate verification.
        """
        
        start_thread = Thread(target=self._CERTIFICATE_Check)
        start_thread.daemon = False  # Ensure thread continues running in the background
        start_thread.start()

    def _CERTIFICATE_Check(self):
        
        """
        Perform the ClientHello and verify the server's certificate.
        """
        
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

        # Receive ServerHello
        server_hello = self.Client.recv(1024)  # Read server response
        print("Client: Received: 'Server Hello'\n")
        data_dict = json.loads(server_hello.decode('utf-8'))  # Decode the JSON response
        for key, value in data_dict.items():
            print(f"{key}: {value}")
        self.Algo_chose = data_dict["encryption"]  # Store the chosen encryption algorithm

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

        # Receive 'Server Done' message
        server_done = self.Client.recv(1024)
        print(f"Client: Received {server_done}")

    def key_exchange(self):
        
        """
        Start a thread to perform the key exchange.
        """
        
        start_thread = Thread(target=self._key_exchange)
        start_thread.daemon = False  # Run in the background
        start_thread.start()

    def _key_exchange(self):
        
        """
        Perform the client-side of the key exchange.
        :return: True if the session key is set, False otherwise.
        """
        
        AES_key = AES_ENCRYPTION.gen_key()  # Generate an AES session key
        self.SESSION_KEY = AES_key  # Store the session key
        encrypt_aes = RSA_ENCRYPTION.encrypt_message(self.SERVER_PUBLIC_KEY.encode().strip(), AES_key)  # Encrypt the session key with the server's public key
        print("Client: Sending exchange key")
        self.Client.sendall(encrypt_aes)  # Send the encrypted session key to the server
        return self.SESSION_KEY is not None

    def final_exchange(self):
        
        """
        Notify the server that the handshake is complete.
        """
        
        self.Client.sendall(b"gChange Cipher Spec + Finished")
        print("Client: Change Cipher Spec + Finished")
        time.sleep(0.1)  # Short delay to ensure message is sent

    def send_a_msg(self, msg):
        
        """
        Encrypt and send a message using the established session key.
        :param msg: The plaintext message to send.
        """
        
        enc_msg = AES_ENCRYPTION.encrypt(self.SESSION_KEY, msg)  # Encrypt the message with AES
        self.Client.sendall(enc_msg)  # Send the encrypted message
