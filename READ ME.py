#togliere il do_GET se non ti serve

"""
si è optato l'utilizzo della libreria socket
per poter effettuare delle simulazioni dei vari handshake e scambio di dati.
esistono anche librerie più primitive che permettono
la creazione di raw packets, come per esempio la libreria scapy
ma è stato evitato, dal momento che:
potrebbe richiedere privilegi elevati
possibili interferenze con altre applicazioni (web browser, client di posta, server web ecc.)
non adatto per applicazioni in tempo reale che richiede una latency bassa

il risultato ottenuto rimane invariato, l'unica differenza è che:
con la libreria socket: la connessione viene stabilita prima per poi simulare quella desiderata
con l liberia scapy: non si stabilisce nessuna connessione, ma vi è una vera e propria costruzione del pacchetto
                    con l' ip, payload ecc. ma, per evitare interferenze su altri computer, non sarà usata

anche se viene stabilita la connessione prima della simulazione, essa rimane costante durante il processo,
rimanendo comunque vedele alla trattazione del problema. Questo porta a un'assimmetria dei print(), ma il flusso logico rimane invariato

"""

