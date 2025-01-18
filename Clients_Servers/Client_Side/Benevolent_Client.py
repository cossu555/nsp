import http.client
import socket
import json
import time
from threading import Thread
import Certificate.Verify_CERTIFICATE as VerifyCertificate
import Encryption.AES_Encryption as AES_ENCRYPTION
import Encryption.RSA_Encryption as RSA_ENCRYPTION

class Benevolent_Client:

    def __init__(self):
        self.Client = None
        self.SERVER_PUBLIC_KEY = None
        self.Algo_chose=None
        self.SESSION_KEY=None

    def http_start(self, server_address, server_port):
        # Create an HTTP connection con il server
        self.Client = http.client.HTTPConnection(server_address, server_port)
        print(f"Client connesso su {server_address}:{server_port}")

    def Send_Message(self, message):
        headers = {'Content-Type': 'text/plain'}
        self.Client.request("POST", "/", body=message, headers=headers)

    def http_end(self):
        self.Client.close()
        self.Client = None

    def TCP_handshake(self,SERVER_ADDRESS, HANDSHAKE_PORT):
        self.Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Client.connect((SERVER_ADDRESS, HANDSHAKE_PORT))  # Connette al server

        # Invia SYN
        self.Client.sendall(b"SYN")
        print("Clinet: Inviato: SYN")

        # Riceve SYN-ACK
        syn_ack = self.Client.recv(1024).decode()
        print(f"Clinet: Ricevuto: {syn_ack}")

        if syn_ack == "SYN-ACK":
            # Invia ACK
            self.Client.sendall(b"ACK")
            print("Clinet: Inviato: ACK")
            return True
        else:
            print("Clinet: errore handshake")
        return False

    def prepare_data(self,START_COMM,CONTENT,VERSION,SESSION_ID,ENCRYPTION,KEY_EXCHANGE,MAC):
        data_dict = {
            "start": START_COMM,
            "content": CONTENT,
            "version": VERSION,
            "session": SESSION_ID,
            "encryption": ENCRYPTION,
            "key_exchange": KEY_EXCHANGE,
            "mac": MAC
        }
        data_bytes = json.dumps(data_dict).encode('utf-8')
        return data_bytes

    def CERTIFICATE_Check(self):
        start_thread = Thread(target=self._CERTIFICATE_Check)
        start_thread.daemon = False
        start_thread.start()

    def _CERTIFICATE_Check(self):
        Client_Hello = self.prepare_data(["START"],
                                   ["Data"],
                                   [1],
                                   [1],
                                   ["AES"],
                                   ["DH"],
                                   ["HMAC"])

        print("Client: invia: 'Client Hello'")
        self.Client.sendall(Client_Hello)

        server_hello = self.Client.recv(1024)
        print("Client: riceve: 'Server Hello'\n")
        data_dict = json.loads(server_hello.decode('utf-8'))
        for key, value in data_dict.items():
            print(f"{key}: {value}")
        self.Algo_chose = data_dict["encryption"]

        print("Client: riceve: 'Certificate' ")
        certificate = self.Client.recv(1024)

        result = VerifyCertificate.verify_certificate(certificate, "server.crt")
        print(f"Client: certificate check: {result}")

        cert_data = VerifyCertificate.get_cert_details(certificate)
        for key, value in cert_data.items():
            print(f"{key}: {value}")

        self.SERVER_PUBLIC_KEY = cert_data["public_key"]

        server_done = self.Client.recv(1024)
        print(f"Client: riceve {server_done}")

    def key_exchange(self):
        start_thread = Thread(target=self._key_exchange)
        start_thread.daemon = False
        start_thread.start()

    def _key_exchange(self):  # Client
        AES_key = AES_ENCRYPTION.gen_key()
        self.SESSION_KEY = AES_key
        encrypt_aes = RSA_ENCRYPTION.encrypt_message(self.SERVER_PUBLIC_KEY.encode().strip(),AES_key)
        print("Client: invia exchange key")
        self.Client.sendall(encrypt_aes)
        if(self.SESSION_KEY != None):
            return True
        return False

    def final_exchange(self):
        self.Client.sendall(b"gChange Cipher Spec + Finished")
        print("Client: Change Cipher Spec + Finisched")
        time.sleep(0.1)

    def send_a_msg(self, msg):
        enc_msg = AES_ENCRYPTION.encrypt(self.SESSION_KEY, msg)
        self.Client.sendall(enc_msg)