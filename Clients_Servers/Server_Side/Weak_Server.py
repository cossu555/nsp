import socket
import threading
import time
from collections import defaultdict


# Starting a server that listens for incoming connections on the specified host and port
def start_server(host, port, secure_mode=False, timeout=30, max_connection_attempts=5):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"server listening on {host}:{port}")

    # Dictionary to track connection attempts (used only in secure mode)
    connection_attempts = defaultdict(int) if secure_mode else None

    try:
        client_socket, client_address = server_socket.accept()
        client_ip = client_address[0]

        # Additional checking  only in secure mode
        if secure_mode:
            connection_attempts[client_ip] += 1

            # Block if too many connection attempts are detected
            if connection_attempts[client_ip] > max_connection_attempts:
                print(f"Connection blocked by the potential attacker {client_ip}")
                client_socket.close()
                return

            # Setting a timeout for receiving data
            client_socket.settimeout(timeout)

            # Attempting to receive data
            try:
                data = client_socket.recv(1024)
                if not data:
                    print(f"Nessun dato ricevuto da {client_ip}")
                    client_socket.close()
                    return

            except socket.timeout:
                print(f"Connessione da {client_ip} scaduta senza inviare dati")
                client_socket.close()
                return

        print(f"Connection Accepted from {client_address}")
        client_socket.close()
    except Exception as e:
        print(f"Errore durante la connessione: {e}")
    finally:
        server_socket.close()
