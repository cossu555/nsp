#pip install cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509 import Name, NameAttribute, CertificateBuilder
from cryptography.x509.oid import NameOID
import datetime

import Encryption.RSA_Encryption as RSA_ENCRYPTION

def gen_certificate(private_key_pem, public_key_pem):
    private_key = serialization.load_pem_private_key(private_key_pem, password=None, backend=default_backend())
    public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())

    subject = Name([NameAttribute(NameOID.COMMON_NAME, u"localhost")])
    issuer = subject
    not_valid_before = datetime.datetime.now(datetime.timezone.utc)
    not_valid_after = not_valid_before + datetime.timedelta(days=365)

    cert_builder = CertificateBuilder(
        subject_name=subject,
        issuer_name=issuer,
        public_key=public_key,
        serial_number=1000,
        not_valid_before=not_valid_before,
        not_valid_after=not_valid_after,
    )

    certificate = cert_builder.sign(
        private_key=private_key,
        algorithm=hashes.SHA256(),
    )

    with open("server.key", "wb") as f:
        f.write(private_key_pem)

    with open("server.crt", "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

    print("Certificato e chiave privata generati con successo!")
    return certificate.public_bytes(serialization.Encoding.PEM)  # Restituisce il certificato

def read_certificate(cert_file_path):
    # Leggi il certificato come byte
    with open(cert_file_path, "rb") as cert_file:
        certificate = cert_file.read()

    return certificate
