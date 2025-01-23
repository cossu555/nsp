# pip install cryptography
# Import necessary modules from the cryptography library
from cryptography.hazmat.backends import default_backend  # Provides cryptographic backends
from cryptography.hazmat.primitives import hashes, serialization  # For hashing and key serialization
from cryptography.x509 import Name, NameAttribute, CertificateBuilder  # For building certificates
from cryptography.x509.oid import NameOID  # For naming standards (e.g., Common Name)
import datetime  # For setting certificate validity dates

# Import a custom RSA encryption module (assumed to be implemented elsewhere)
import Encryption.RSA_Encryption as RSA_ENCRYPTION


# Generating a self-signed X.509 certificate using a given private and public key
def gen_certificate(private_key_pem, public_key_pem):
    # Deserialize the private key from PEM format to a usable object
    private_key = serialization.load_pem_private_key(
        private_key_pem,  # The PEM-formatted private key
        password=None,  # Assumes the private key is unencrypted
        backend=default_backend()  # Specifies the backend to use
    )

    # Deserialize the public key from PEM format to a usable object
    public_key = serialization.load_pem_public_key(
        public_key_pem,  # The PEM-formatted public key
        backend=default_backend()  # Specifies the backend to use
    )

    # Create a "subject" name for the certificate (here it's self-signed, so issuer = subject)
    subject = Name([NameAttribute(NameOID.COMMON_NAME, u"localhost")])  # Sets Common Name to "localhost"
    issuer = subject  # Since this is a self-signed certificate, issuer is the same as subject

    # Set certificate validity period
    not_valid_before = datetime.datetime.now(datetime.timezone.utc)  # Current UTC time
    not_valid_after = not_valid_before + datetime.timedelta(days=365)  # Valid for 1 year

    # Initialize a certificate builder with required attributes
    cert_builder = CertificateBuilder(
        subject_name=subject,  # Subject name of the certificate
        issuer_name=issuer,  # Issuer name (self-signed)
        public_key=public_key,  # The public key associated with the certificate
        serial_number=1000,  # A unique serial number for the certificate
        not_valid_before=not_valid_before,  # Start of validity period
        not_valid_after=not_valid_after,  # End of validity period
    )

    # Sign the certificate with the private key and SHA-256 hashing algorithm
    certificate = cert_builder.sign(
        private_key=private_key,  # The private key used to sign the certificate
        algorithm=hashes.SHA256(),  # Hashing algorithm for the signature
    )

    # Save the private key to a file
    with open("server.key", "wb") as f:
        f.write(private_key_pem)  # Write the private key in PEM format to "server.key"

    # Save the certificate to a file
    with open("server.crt", "wb") as f:
        f.write(
            certificate.public_bytes(serialization.Encoding.PEM))  # Write the certificate in PEM format to "server.crt"

    print("Certificate and private key successfully generated!")  # Notify user of successful generation

    # Return the generated certificate in PEM format
    return certificate.public_bytes(serialization.Encoding.PEM)


# Reading a certificate from a file
def read_certificate(cert_file_path):
    # Open the certificate file in binary mode and read its contents
    with open(cert_file_path, "rb") as cert_file:
        certificate = cert_file.read()  # Read the entire certificate file into memory

    return certificate  # Return the certificate content as bytes
