# data_holder.py
import json
import base64
import hmac
import hashlib
from datetime import datetime, timezone

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import oqs


class DataHolder:
    """
    A post-quantum Data Holder who receives a signed permit
    verifies, recovers the master secret K, and pseudonymizes identifiers.
    """

    def __init__(self, name: str, kem_secret_key: bytes):
        self.name = name
        self.kem = oqs.KeyEncapsulation("ML-KEM-768", kem_secret_key)

    def _verify_permit(self, signed_permit: dict) -> dict:
        """Verifieer de ML-DSA handtekening van de issuer."""
        payload_str = signed_permit["payload"]
        payload_bytes = payload_str.encode("utf-8")
        signature = base64.b64decode(signed_permit["signature_base64"])
        verification_key = base64.b64decode(signed_permit["issuer_verification_key_base64"])

        verifier = oqs.Signature("ML-DSA-65")
        if not verifier.verify(payload_bytes, signature, verification_key):
            raise ValueError("Invalid permit signature")

        return json.loads(payload_str)

    def _recover_master_k(self, permit_payload: dict) -> bytes:
        """Herstel de gedeelde master secret K via ML-KEM decapsulatie + AES-GCM decryptie."""
        for entry in permit_payload["encrypted_keys"]:
            if entry["holder_name"] == self.name:
                kem_ciphertext = base64.b64decode(entry["kem_ciphertext_base64"])
                nonce = base64.b64decode(entry["nonce_base64"])
                encrypted_master_k = base64.b64decode(entry["encrypted_master_k_base64"])

                # 1. Decapsuleer om de holder-specifieke shared secret S_i te krijgen
                shared_secret_si = self.kem.decap_secret(kem_ciphertext)

                # 2. Afleiden van dezelfde AES-256 sleutel
                aes_key = hashlib.sha256(shared_secret_si).digest()

                # 3. Decrypt de master K
                aesgcm = AESGCM(aes_key)
                master_k = aesgcm.decrypt(nonce, encrypted_master_k, None)  # geen AAD

                return master_k

        raise ValueError(f"No encrypted key entry found for holder {self.name}")

    def pseudonymize_identifier(self, identifier: str, domain: str, K: bytes) -> str:
        """Deterministische pseudonym met HMAC-SHA256."""
        message = (identifier + domain).encode("utf-8")
        return hmac.new(K, message, hashlib.sha256).hexdigest()

    def process_permit_and_pseudonymize(
        self,
        signed_permit_json: bytes,
        identifiers: list[str]
    ) -> list[str]:
        """Volledig proces: verifiëren → expiratie check → K herstellen → pseudonimiseren."""
        signed_permit = json.loads(signed_permit_json.decode("utf-8"))
        permit_payload = self._verify_permit(signed_permit)

        # Expiratie controle
        valid_until = datetime.fromisoformat(permit_payload["valid_until"])
        if valid_until < datetime.now(timezone.utc):
            raise ValueError("Permit has expired")

        # Herstel master K en pseudonimiseer
        master_K = self._recover_master_k(permit_payload)
        domain = permit_payload["domain"]

        return [self.pseudonymize_identifier(id_, domain, master_K) for id_ in identifiers]