import Clients_Servers.Server_Side.Weak_Server as W_S

host = input("Enter for server side: (suggestion: 0.0.0.0)")
port = int(input("Enter port: (suggestion: 443)"))

W_S._start_server(host, port)
