# Import needed libraries
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Function to generate a pair of RSA keys
def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key
def encrypt_message(public_key, message):
    # Use RSA key to encrypt AES key
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
    encrypted_message = cipher_rsa.encrypt(message)
    return encrypted_message

def decrypt_message(private_key, encrypted_message):
    # Use RSA key to decrypt AES key
    cipher_rsa_private = PKCS1_OAEP.new(RSA.import_key(private_key))
    decrypted_message = cipher_rsa_private.decrypt(encrypted_message)
    return decrypted_message

