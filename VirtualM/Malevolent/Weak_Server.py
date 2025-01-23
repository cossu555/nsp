import Clients_Servers.Server_Side.Weak_Server as W_S

host = input("Enter host: (suggestion: 172.20.10.13)")
port = int(input("Enter port: (suggestion: 443)"))

W_S.start_server(host, port)
