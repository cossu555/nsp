# Import needed libraries
import Clients_Servers.Client_Side.Malevolent_Client as M_C

ip = input("Insert IP to attack: (suggestion 172.20.10.13)")
port = int(input("Insert port to attack: (suggesstion 443)"))
N = int(input("Insert number of attempts"))

M_C._connect_to_server(ip,port, num_attempts=N, delay=1)