# Import needed libraries
import socket
import threading
import time

# Legitimate client
def legitimate_client():
    time.sleep(2)  # Wait in order to let the malicious client connect before
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 443))  # Connection to the server
        s.sendall(b'Hello from the legitimate client!')
        data = s.recv(1024)
        print(f'Legitimate client received: {data.decode()}')

# Malicious client
def malicious_client():
    # It connect to the server as MitM
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_to_server:
        client_to_server.connect(('localhost', 443))
        print('Malicious client connected to server')

        # Start the intermediate server for the legitimate client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as mitm_server:
            mitm_server.bind(('localhost', 4443))  # MitM's port
            mitm_server.listen(1)
            print('Malicious client is ready to intercept messages')

            conn, addr = mitm_server.accept()
            print(f'Connection from legitimate client at {addr}')

            # Forward loop: interept messages
            while True:
                data_from_legitimate = conn.recv(1024)
                if not data_from_legitimate:
                    break
                print(f'Malicious client intercepted: {data_from_legitimate.decode()}')
                client_to_server.sendall(data_from_legitimate)  # Send to server

                data_from_server = client_to_server.recv(1024)
                print(f'Malicious client received from server: {data_from_server.decode()}')
                conn.sendall(data_from_server)  # Send to the legitimate client

            print('Malicious client finished interception')

# Start of the testing
def main():
    # Thread for the malicious client
    malicious_thread = threading.Thread(target=malicious_client)
    malicious_thread.start()

    # Thread for the legitimate client
    legitimate_thread = threading.Thread(target=legitimate_client)
    legitimate_thread.start()

    # Wait the end of both threads
    malicious_thread.join()
    legitimate_thread.join()

if __name__ == '__main__':
    main()
