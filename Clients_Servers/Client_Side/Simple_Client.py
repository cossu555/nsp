import socket
import ssl

def second_client_attempt(host, port):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as s:
            with context.wrap_socket(s, server_hostname=host) as ssl_sock:
                print("Client Benevolo: Second client connected to server.")
                request = f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n"
                ssl_sock.sendall(request.encode())
                response = ssl_sock.recv(1024)
                print(f"Client Benevolo:Second client received: {response.decode()}")
    except Exception as e:
        print(f"Client Benevolo: Second client failed to connect: {e}")