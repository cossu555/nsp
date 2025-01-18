#pip install cryptography
from cryptography.hazmat.backends import default_backend
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.primitives import serialization
import datetime

def verify_certificate(cert_data, trusted_cert_file_path):
    # Carica il certificato ricevuto
    certificate = x509.load_pem_x509_certificate(cert_data)

    # Carica il certificato della CA fidata
    with open(trusted_cert_file_path, "rb") as f:
        trusted_cert_data = f.read()
    trusted_certificate = x509.load_pem_x509_certificate(trusted_cert_data)

    # Verifica la firma del certificato
    try:
        trusted_certificate.public_key().verify(
            certificate.signature,
            certificate.tbs_certificate_bytes,
            padding.PKCS1v15(),
            certificate.signature_hash_algorithm
        )
    except Exception as e:
        return False #"Verifica della firma fallita"

    # Controllo della data di validità
    current_time = datetime.datetime.now(datetime.UTC)
    if certificate.not_valid_before_utc > current_time or certificate.not_valid_after_utc < current_time:
        return False #"Certificato non valido temporalmente."

    return True #"Certificato verificato con successo."

def get_cert_details(cert_data):
    cert = load_pem_x509_certificate(cert_data, default_backend())

    public_key_pem = cert.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    cert_details = {
        'subject_name': cert.subject,
        'issuer_name': cert.issuer,
        'public_key': public_key_pem.decode(),
        'serial_number': cert.serial_number,
        'not_valid_before': cert.not_valid_before_utc,
        'not_valid_after': cert.not_valid_after_utc
    }

    return cert_details
