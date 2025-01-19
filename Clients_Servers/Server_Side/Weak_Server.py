import socket
from threading import Thread

def start_server(host, port):
    start_thread = Thread(target=_start_server, args=(host, port))
    start_thread.daemon = True
    start_thread.start()

def _start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)  # Consente una connessione in attesa
        print(f"Server in ascolto su {host}:{port}")

        while True:
            print("In attesa di una connessione...")
            conn, addr = server_socket.accept()  # Accetta una connessione
            with conn:
                print(f"Connesso a {addr}")
                handle_client(conn)
                print(f"Connessione chiusa con {addr}")

def handle_client(conn):
    while True:
        data = conn.recv(1024)  # Riceve dati dal client
        if not data:
            break  # Interrompe se non ci sono dati
        print(f"Ricevuto: {data.decode('utf-8')}")
        conn.sendall(b"Ricevuto")  # Invia una risposta al client
