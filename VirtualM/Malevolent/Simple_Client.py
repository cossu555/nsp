import Clients_Servers.Client_Side.Simple_Client as S_C


host = input("Enter host: (suggestion: 172.20.10.13)  ")
port= int(input("Enter port: (suggestion: 443)"))

S_C.second_client_attempt(host,port)

