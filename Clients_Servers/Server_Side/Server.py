# Import needed libraries 
import socket
import socketserver
import json
from threading import Thread
from Clients_Servers.Server_Side.MyHandler_Class import MyHandler  # Import MyHandler for HTTP handling
from Certificate import Create_CERTIFICATE as CreateCertificate  # Import certificate creation module
from Encryption import RSA_Encryption as rsa  # Import RSA encryption module
from Encryption import AES_Encryption as aes  # Import AES encryption module
import time

class Server:

    def __init__(self, MY_IP_ADDRESS='127.0.0.1'):
        
        """
        Initialize the server with default settings.
        - Generate RSA private and public keys.
        - Generate a self-signed certificate using the keys.
        """
        
        self.MY_IP_ADDRESS = MY_IP_ADDRESS
        self.server_conn = None  # Placeholder for the client connection
        self.Client_Algo = None  # Placeholder for the encryption algorithm chosen by the client
        self.SESSION_KEY = None  # Placeholder for the session key

        # Generate RSA key pair
        self.PRIVATE_KEY, self.PUBLIC_KEY = rsa.generate_keys()

        # Generate a self-signed certificate
        self.CERTIFICATE = CreateCertificate.gen_certificate(self.PRIVATE_KEY, self.PUBLIC_KEY)

    def startHTTP(self, PORT=80, IPS=""):
        
        """
        Start an HTTP server on a separate thread.
        """
        
        start_thread = Thread(target=self._start_HTTPserver, args=(PORT, IPS))
        start_thread.daemon = False  # Keeps the thread alive
        start_thread.start()

    def _start_HTTPserver(self, PORT=80, IPS=""):
        
        """
        Actual method to start the HTTP server.
        - Binds the server to the specified IP and port.
        """
        
        httpd = socketserver.TCPServer((IPS, PORT), MyHandler)
        print(f"Server started on {self.MY_IP_ADDRESS}:{PORT}")
        httpd.serve_forever()

    def TCP_handshake(self, MY_IP_ADDRESS, HANDSHAKE_PORT):
        
        """
        Start the TCP handshake process in a separate thread.
        """
        
        start_thread = Thread(target=self._TCP_handshake, args=(MY_IP_ADDRESS, HANDSHAKE_PORT))
        start_thread.daemon = False
        start_thread.start()

    def _TCP_handshake(self, MY_IP_ADDRESS, HANDSHAKE_PORT):
        
        """
        Perform a TCP three-way handshake:
        - SYN -> SYN-ACK -> ACK
        """
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((MY_IP_ADDRESS, HANDSHAKE_PORT))  # Bind the socket to the IP and port

        server_socket.listen()  # Put the socket in listening mode
        print("Server listening")

        conn, addr = server_socket.accept()  # Accept an incoming connection

        # Receive SYN from the client
        syn = conn.recv(1024).decode()
        print(f"Server: Received: {syn}")

        if syn == "SYN":
            # Send SYN-ACK back to the client
            conn.sendall(b"SYN-ACK")
            print("Server: Sent: SYN-ACK")

            # Receive ACK from the client
            ack = conn.recv(1024).decode()
            print(f"Server: Received: {ack}")

            if ack == "ACK":
                print("Server: Handshake completed!")
                self.server_conn = conn  # Save the connection for further communication
                return True
        print("Server: Handshake error")
        return False

    def CHERTIFICATE_check(self):
        
        """
        Perform certificate exchange:
        - Server sends 'Server Hello' with encryption details.
        - Sends its certificate to the client.
        """
        
        # Receive 'Client Hello' message
        client_hello = self.server_conn.recv(1024)
        print(f"Server: Received 'Client Hello'\n")

        # Analyze 'Client Hello' data
        data_dict = json.loads(client_hello.decode('utf-8'))
        server_hello = {}
        for key, value in data_dict.items():
            print(f"{key}: {value}")
            # Server selects the first proposed option for simplicity
            server_hello[key] = value[0]

        # Send 'Server Hello' with selected options
        print("Server: Sending 'Server Hello'\n")
        self.server_conn.sendall(json.dumps(server_hello).encode('utf-8'))

        # Send the server's certificate
        print("Server: Sending 'Certificate'\n")
        self.server_conn.sendall(self.CERTIFICATE)

        # Notify the client that the server hello phase is done
        print("Server: Sending 'Server Hello Done'\n")
        self.server_conn.sendall(b"ServerHelloDone, Connection ready for the client\n")

    def key_exchange(self):  # Server
        
        """
        Perform key exchange:
        - Server receives the AES key encrypted with its public key.
        - Decrypts the key using its private RSA key.
        """
        
        # Receive the encrypted AES key from the client
        aes_enc = self.server_conn.recv(1024)
        aes_decrypt = rsa.decrypt_message(self.PRIVATE_KEY, aes_enc)  # Decrypt the AES key
        self.SESSION_KEY = aes_decrypt  # Store the session key
        print("Server: Received the encrypted key")

        if self.SESSION_KEY is not None:
            return True
        return False

    def final_exchange(self):
        
        """
        Perform the final handshake phase:
        - Receive and respond with 'Change Cipher Spec + Finished'.
        """
        
        msg = self.server_conn.recv(1024)  # Receive final message from client
        self.server_conn.sendall(b"gChange Cipher Spec + Finished")  # Respond to the client
        print("Server: Change Cipher Spec + Finished")

    def recieve_msg(self):
        
        """
        Receive and decrypt a message from the client:
        - Uses the session key to decrypt the incoming message.
        """
        
        # Receive the encrypted message from the client
        msg = self.server_conn.recv(1024)
        print(f"Server: Received the message: {msg}")

        # Decrypt the message using AES and the session key
        dec_msg = aes.decrypt(self.SESSION_KEY, msg)
        print(f"Server: Decrypted: {dec_msg}")
