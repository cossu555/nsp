import time

import Clients_Servers.Client_Side.Malevolent_Clinet as M_C
import Clients_Servers.Client_Side.Simple_Client as S_C
import Clients_Servers.Server_Side.Weak_Server as W_S

server_host = "127.0.0.1"  # Sostituisci con l'indirizzo del server
server_port = 443

M_C.connect_to_server(server_host, server_port)
time.sleep(10)
W_S.start_server(server_host, server_port)
time.sleep(10)
S_C.second_client_attempt(server_host, server_port)
