#pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Genera una chiave AES casuale
def gen_key():
    return get_random_bytes(32)  # 256-bit key

# Funzione di cifratura
def encrypt(key, data):
    iv = get_random_bytes(AES.block_size)  # IV casuale
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Pad e cifra i dati
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return iv + encrypted_data  # Restituisce IV + dati cifrati

# Funzione di decrittazione
def decrypt(key, encrypted_data):
    iv = encrypted_data[:AES.block_size]  # Estrai l'IV
    cipher_text = encrypted_data[AES.block_size:]  # I dati cifrati
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decifra e rimuovi il padding
    decrypted_data = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return decrypted_data.decode()  # Decodifica i dati in formato stringa

