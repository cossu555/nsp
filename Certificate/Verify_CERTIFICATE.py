# pip install cryptography
# Import required modules from the cryptography library
from cryptography.hazmat.backends import default_backend  # Provides cryptographic backends
from cryptography import x509  # For handling X.509 certificates
from cryptography.hazmat.primitives.asymmetric import padding  # For cryptographic padding schemes
from cryptography.x509 import load_pem_x509_certificate  # For loading X.509 certificates
from cryptography.hazmat.primitives import serialization  # For serialization of public keys
import datetime  # For managing and comparing certificate validity periods


# Verifying a certificate against a trusted Certificate Authority
def verify_certificate(cert_data, trusted_cert_file_path):
    try:
        # Load the provided certificate from PEM format
        certificate = x509.load_pem_x509_certificate(cert_data)

        # Load the trusted CA certificate from the file
        with open(trusted_cert_file_path, "rb") as f:
            trusted_cert_data = f.read()  # Read the trusted CA certificate as bytes
        trusted_certificate = x509.load_pem_x509_certificate(trusted_cert_data)  # Analyze the CA certificate

        # Verify the signature of the provided certificate using the trusted CA's public key
        try:
            trusted_certificate.public_key().verify(
                certificate.signature,  # The signature from the provided certificate
                certificate.tbs_certificate_bytes,  # The certificate's data to be signed
                padding.PKCS1v15(),  # Use PKCS1 v1.5 padding (common for certificates)
                certificate.signature_hash_algorithm  # The hash algorithm used for the signature
            )
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False  # If the verification fails, return False

        # Verify the certificate's validity period (current time must be within the valid range)
        current_time = datetime.datetime.now(datetime.UTC)  # Get the current time in UTC
        if certificate.not_valid_before_utc > current_time or certificate.not_valid_after_utc < current_time:
            return False  # Certificate is not valid either because it's expired or not yet valid

        return True  # Certificate is verified successfully

    except FileNotFoundError as e:
        print(f"Error: The file '{trusted_cert_file_path}' was not found. {e}")
        return False
    except ValueError as e:
        print(f"Error: Value error occurred while processing the certificate. {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


# Extract details from a certificate
def get_cert_details(cert_data):
    try:
        # Load the certificate from PEM format
        cert = load_pem_x509_certificate(cert_data, default_backend())

        # Extract the public key in PEM format
        public_key_pem = cert.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,  # Use PEM encoding
            format=serialization.PublicFormat.SubjectPublicKeyInfo  # Standard public key info format
        )

        # Extract key details from the certificate
        cert_details = {
            'subject_name': cert.subject,  # The subject (e.g., the entity the certificate represents)
            'issuer_name': cert.issuer,  # The issuer (e.g., the Certificate Authority)
            'public_key': public_key_pem.decode(),  # The public key associated with the certificate
            'serial_number': cert.serial_number,  # The certificate's unique serial number
            'not_valid_before': cert.not_valid_before_utc,  # Start of the certificate's validity period
            'not_valid_after': cert.not_valid_after_utc  # End of the certificate's validity period
        }

        return cert_details  # Return the extracted details as a dictionary

    except ValueError as e:
        print(f"Error: Value error occurred while loading or processing the certificate. {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
