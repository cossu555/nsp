# Import needed libraries
from Clients_Servers.Server_Side.Server import Server
import socket
import json


class VMServer(Server):

    def VM_start_conn(self,ip,port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_socket.bind((ip, port))
        server_socket.listen(1)
        print(f"server listening on {ip}:{port}")

        client_socket, client_address = server_socket.accept()

        print(f"Connection Accepted from {client_address}")
        self.server_conn=client_socket

    def VM_CHERTIFICATE_check(self):
        """
        Perform certificate exchange:
        - Server sends 'Server Hello' with encryption details.
        - Sends its certificate to the client.
        """

        # Receive 'Client Hello' message
        client_hello = self.server_conn.recv(1024)
        print(f"Server: Received 'Client Hello'\n")

        # Analyze 'Client Hello' data
        data_dict = json.loads(client_hello.decode('utf-8'))
        server_hello = {}
        for key, value in data_dict.items():
            print(f"{key}: {value}")
            # Server selects the first proposed option for simplicity
            server_hello[key] = value[0]

        input("Press Enter to continue(2)")

        # Send 'Server Hello' with selected options
        print("Server: Sending 'Server Hello'\n")
        self.server_conn.sendall(json.dumps(server_hello).encode('utf-8'))

        input("Press Enter to continue(4)")

        # Send the server's certificate
        print("Server: Sending 'Certificate'\n")
        self.server_conn.sendall(self.CERTIFICATE)

        input("Press Enter to continue(6)")

        # Notify the client that the server hello phase is done
        print("Server: Sending 'Server Hello Done'\n")
        self.server_conn.sendall(b"ServerHelloDone\n")


