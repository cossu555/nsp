import socket
def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"server listening on {host}:{port}")

    client_socket,client_address = server_socket.accept()

    print(f"Connection Accepted from {client_address}")
    client_socket.close()
    server_socket.close()
