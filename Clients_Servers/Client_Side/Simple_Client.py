import socket
import time
from threading import Thread

# Durata del blocco in secondi
BLOCK_DURATION = 60  # Ad esempio, 60 secondi

def start_server(host, port):
    start_thread = Thread(target=_start_server, args=(host, port))
    start_thread.daemon = True      # Ensure the thread will not block program exit
    start_thread.start()

def _start_server(host, port):
    # Dizionario per tenere traccia degli IP bloccati
    blocked_ips = {}

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Permette fino a 5 connessioni in coda
    print(f"Server listening on {host}:{port}")

    while True:
        # Accetta una nuova connessione
        client_socket, client_address = server_socket.accept()
        client_ip, client_port = client_address

        # Controlla se l'IP è bloccato
        current_time = time.time()
        if client_ip in blocked_ips:
            # Verifica se il tempo di blocco è terminato
            if current_time < blocked_ips[client_ip]:
                print(f"Connection denied for {client_ip}. IP is temporarily blocked.")
                client_socket.close()
                continue
            else:
                # Sblocca l'IP se il tempo di blocco è scaduto
                del blocked_ips[client_ip]

        # Connessione accettata
        print(f"Connection accepted from {client_ip}:{client_port}")
        print("Server received:", client_socket.recv(1024))
        client_socket.close()

        # Blocca l'IP per il tempo specificato
        blocked_ips[client_ip] = current_time + BLOCK_DURATION
        print(f"IP {client_ip} is now blocked for {BLOCK_DURATION} seconds.")

