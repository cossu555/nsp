import http.client
import time

def persistent_connection_to_server():

    # Questo client tenta continuamente di connettersi alla porta 443 del server fino a quando non riesce.
    # Una volta connesso, invia una richiesta e riceve una risposta.
    while True:
        try:
            # Tenta di connettersi al server sulla porta 443 (HTTPS)
            print("Tentativo di connessione al server sulla porta 443...")
            conn = http.client.HTTPSConnection("127.0.0.1", 443, timeout=5)  # Modifica l'host se necessario
            conn.request("GET", "/")  # Invia una semplice richiesta GET

            # Recupera la risposta
            response = conn.getresponse()
            print(f"Connesso con successo! Risposta del server: {response.status} - {response.reason}")
            print("Contenuto della risposta:", response.read().decode())

            conn.close()
            break  # Esci dal ciclo una volta stabilita la connessione
        except Exception as e:
            print(f"Errore durante la connessione: {e}. Riprovo tra 1 secondo...")
            time.sleep(1)  # Aspetta un secondo prima di riprovare

if __name__ == "__main__":
    persistent_connection_to_server()
