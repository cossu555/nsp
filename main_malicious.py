# Import needed library
import time

# Import the malevolent client, simple client, and weak server implementations
import Clients_Servers.Client_Side.Malevolent_Client as M_C
import Clients_Servers.Client_Side.Simple_Client as S_C
import Clients_Servers.Server_Side.Weak_Server as W_S

# Define the server's host address and port number
server_host = "127.0.0.1"  # Replace with the server's actual address
server_port = 443          # Standard HTTPS port for secure communication

# Step 1: Start the connection from the malevolent client
# This client attempts to connect to the server before other clients
M_C.connect_to_server(server_host, server_port)
time.sleep(25)  # Allow some time for the connection to establish

# Step 2: Start the weak server with secure mode
# The server listens on the defined host and port for incoming connections
W_S.start_server(server_host, server_port, secure_mode=True)
time.sleep(10)  # Allow the server some time to initialize and begin listening

# Step 3: A second client attempts to connect
# This represents a normal client trying to communicate with the server
S_C.second_client_attempt(server_host, server_port)
