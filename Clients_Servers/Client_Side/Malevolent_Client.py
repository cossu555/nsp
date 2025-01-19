import socket
import time
from threading import Thread
def connect_to_server(host, port):
    start_thread = Thread(target=_connect_to_server, args=(host, port))
    start_thread.daemon = True
    start_thread.start()

def _connect_to_server(host, port):
    while True:
        try:
            with socket.create_connection((host, port), timeout=5) as s:
                print(f"Client Malevolo: Connesso con successo a {host} sulla porta {port}.")
                break
        except (socket.timeout, ConnectionRefusedError) as e:
            print(f"Client Malevolo: Connessione fallita: {e}. Ritento...")
            time.sleep(5)
