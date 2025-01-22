# Import needed libraries
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Function to generate a pair of RSA keys
def generate_keys():
    try:
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key
    except Exception as e:
        print(f"Error generating RSA keys: {e}")
        return None, None

# Function to encrypt a message using the public key
def encrypt_message(public_key, message):
    try:
        if not isinstance(message, bytes):
            message = message.encode('utf-8')  # Ensure the message is in bytes

        cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
        encrypted_message = cipher_rsa.encrypt(message)
        return encrypted_message
    except ValueError as ve:
        print(f"Value error during encryption: {ve}")
    except Exception as e:
        print(f"Error encrypting message: {e}")
    return None

# Function to decrypt a message using the private key
def decrypt_message(private_key, encrypted_message):
    # Use RSA key to decrypt AES key
    cipher_rsa_private = PKCS1_OAEP.new(RSA.import_key(private_key))
    decrypted_message = cipher_rsa_private.decrypt(encrypted_message)
    return decrypted_message
