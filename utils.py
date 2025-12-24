# utils.py
import oqs

def generate_ml_kem_keypair():
    """Generate ML-KEM-768 keypair."""
    kem = oqs.KeyEncapsulation("ML-KEM-768")
    public_key = kem.generate_keypair()
    secret_key = kem.export_secret_key()
    return {"public_key": public_key, "secret_key": secret_key}

def generate_ml_dsa_keypair():
    """Generate ML-DSA-65 keypair."""
    sig = oqs.Signature("ML-DSA-65")
    public_key = sig.generate_keypair()
    secret_key = sig.export_secret_key()
    return {"public_key": public_key, "secret_key": secret_key}