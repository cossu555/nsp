import Clients_Servers.Client_Side.Simple_Client as S_C



ip = input("Insert IP to access: (suggestion 172.20.10.13)")
port = int(input("Insert port to access: (suggesstion 443)"))


S_C.second_client_attempt(ip,port)

