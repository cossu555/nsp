import socket
import socketserver
import json
from threading import Thread
from Clients_Servers.Server_Side.MyHandler_Class import MyHandler  # Import MyHandler from MyHandler_Class
from Certificate import Create_CERTIFICATE as CreateCertificate
from Encryption import RSA_Encryption as rsa
from Encryption import AES_Encryption as aes
import time
class Server:

    def __init__(self, MY_IP_ADDRESS = '127.0.0.1'):
        self.MY_IP_ADDRESS = MY_IP_ADDRESS
        self.server_conn = None
        self.Client_Algo = None
        self.SESSION_KEY = None

        self.PRIVATE_KEY, self.PUBLIC_KEY = rsa.generate_keys()
        self.CERTIFICATE = CreateCertificate.gen_certificate(self.PRIVATE_KEY, self.PUBLIC_KEY)

    def startHTTP(self, PORT=80, IPS = ""):
        start_thread = Thread(target=self._start_HTTPserver, args=(PORT, IPS))
        start_thread.daemon = False
        start_thread.start()

    def _start_HTTPserver(self, PORT=80, IPS = ""):
        httpd = socketserver.TCPServer((IPS, PORT), MyHandler)

        print(f"Server avviato su {self.MY_IP_ADDRESS}:{PORT}")
        httpd.serve_forever()

    def TCP_handshake(self,MY_IP_ADDRESS, HANDSHAKE_PORT):
        start_thread = Thread(target=self._TCP_handshake, args=(MY_IP_ADDRESS,HANDSHAKE_PORT))
        start_thread.daemon = False
        start_thread.start()

    def _TCP_handshake(self, MY_IP_ADDRESS, HANDSHAKE_PORT):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((MY_IP_ADDRESS, HANDSHAKE_PORT))  # Assegna l'indirizzo IP e la porta

        server_socket.listen()  # Mette il socket in ascolto
        print("Server in ascolto")

        conn, addr = server_socket.accept()

        # Riceve SYN
        syn = conn.recv(1024).decode()
        print(f"Server: Ricevuto: {syn}")

        if syn == "SYN":
            # Invia SYN-ACK
            conn.sendall(b"SYN-ACK")
            print("Server: Inviato: SYN-ACK")

            # Riceve ACK
            ack = conn.recv(1024).decode()
            print(f"Server: Ricevuto: {ack}")

            if ack == "ACK":
                print("Server: Handshake completato!")
                self.server_conn = conn
                return True
        print("Server: errore handshake")
        return False

    def CHERTIFICATE_check(self):
        client_hello = self.server_conn.recv(1024)
        print(f"Server: riceve 'Client Hello'\n")

        data_dict = json.loads(client_hello.decode('utf-8'))
        server_hello = {}
        # Stampa e salva i dati ricevuti
        for key, value in data_dict.items():
            print(f"{key}: {value}")
            server_hello[key] = value[0] #per semplificare, la policy del server sarà quella di scegliee sempre la prima propsta del client

        print("Server: invia 'Server Hello'\n")
        self.server_conn.sendall(json.dumps(server_hello).encode('utf-8'))

        print("Server: invia 'Certificate'\n")
        self.server_conn.sendall(self.CERTIFICATE)
        print("Server: invia 'Server Hello Done'\n")
        self.server_conn.sendall(b"ServerHelloDone, Connessione pronta per il client\n")


    def key_exchange(self):  # Server
        aes_enc = self.server_conn.recv(1024)
        aes_decrypt = rsa.decrypt_message(self.PRIVATE_KEY, aes_enc)
        self.SESSION_KEY = aes_decrypt
        print("Server: riceve la encrypted key")

        if(self.SESSION_KEY != None):
            return True
        return False

    def final_exchange(self):
        msg=self.server_conn.recv(1024)
        self.server_conn.sendall(b"gChange Cipher Spec + Finished")
        print("Server: Change Cipher Spec + Finisched")

    def recieve_msg(self):
        msg = self.server_conn.recv(1024)
        print(f"Server: riceve il messaggio:{msg}")
        dec_msg = aes.decrypt(self.SESSION_KEY, msg)
        print(f"Server: decrypta: {dec_msg}")