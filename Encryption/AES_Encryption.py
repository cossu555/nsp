#pip install pycryptodome
# Import needed libraries
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Generate a random AES key
def gen_key():
    try:
        return get_random_bytes(32)  # 256-bit key
    except Exception as e:
        print(f"Error generating AES key: {e}")
        return None

# Encryption function
def encrypt(key, data):
    try:
        if not isinstance(data, str):
            raise ValueError("Data to encrypt must be a string.")

        iv = get_random_bytes(AES.block_size)  # IV random
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # Padding and encryption of the data
        encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
        return iv + encrypted_data
    except ValueError as ve:
        print(f"Value error during encryption: {ve}")
    except Exception as e:
        print(f"Error encrypting data: {e}")
    return None

# Decryption function
def decrypt(key, encrypted_data):
    iv = encrypted_data[:AES.block_size]  # Extract the IV
    cipher_text = encrypted_data[AES.block_size:]  # Encrypted data
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # Decrypt and remove the padding
    decrypted_data = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return decrypted_data.decode()  # Decode the data into string form
