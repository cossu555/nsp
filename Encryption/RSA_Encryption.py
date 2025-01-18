from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Funzione per generare una coppia di chiavi RSA
def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key
def encrypt_message(public_key, message):
    # Usa la chiave RSA per cifrare una chiave AES
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_message = cipher_rsa.encrypt(message)
    return encrypted_message

def decrypt_message(private_key, encrypted_message):
    # Usa la chiave RSA privata per decifrare la chiave AES
    cipher_rsa_private = PKCS1_OAEP.new(RSA.import_key(private_key))
    decrypted_message = cipher_rsa_private.decrypt(encrypted_message)
    return decrypted_message

