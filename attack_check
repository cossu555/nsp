import socket
import threading
import time

# Client benevolo
def benevolent_client():
    time.sleep(2)  # Attende per far partire il client malevolo prima
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 443))  # Connettiti al server
        s.sendall(b'Hello from the benevolent client!')
        data = s.recv(1024)
        print(f'Benevolent client received: {data.decode()}')

# Client malevolo
def malicious_client():
    # Si connette al server come MITM
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_to_server:
        client_to_server.connect(('localhost', 443))
        print('Malicious client connected to server')

        # Avvia il server intermedio per il benevolo
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mitm_server:
            mitm_server.bind(('localhost', 4443))  # Porta MITM
            mitm_server.listen(1)
            print('Malicious client is ready to intercept messages')

            conn, addr = mitm_server.accept()
            print(f'Connection from benevolent client at {addr}')

            # Forward loop: intercetta i messaggi
            while True:
                data_from_benevolent = conn.recv(1024)
                if not data_from_benevolent:
                    break
                print(f'Malicious client intercepted: {data_from_benevolent.decode()}')
                client_to_server.sendall(data_from_benevolent)  # Invio al server

                data_from_server = client_to_server.recv(1024)
                print(f'Malicious client received from server: {data_from_server.decode()}')
                conn.sendall(data_from_server)  # Invio al client benevolo

            print('Malicious client finished interception')

# Avvio del test
def main():
    # Thread per il client malevolo
    malicious_thread = threading.Thread(target=malicious_client)
    malicious_thread.start()

    # Thread per il client benevolo
    benevolent_thread = threading.Thread(target=benevolent_client)
    benevolent_thread.start()

    # Attendi la fine di entrambi i thread
    malicious_thread.join()
    benevolent_thread.join()

if __name__ == '__main__':
    main()
