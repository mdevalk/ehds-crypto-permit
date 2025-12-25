# data_permit_issuer.py
import os
import json
import base64
import hashlib
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import oqs

class DataPermitIssuer:
    """
    A minimal post-quantum permit issuer (HDAB)
    """

    def __init__(self, issuer_secret_key: bytes):
        self.sig = oqs.Signature("ML-DSA-65", issuer_secret_key)

    def issue_data_permit(
        self,
        permit_id: str,
        domain: str,
        data_holders: list[dict],
        issuer_public_key: bytes,
        validity_years: int = 1,
        include_raw_k: bool = False
    ) -> dict:
        # Generate master shared secret K
        master_K = os.urandom(32)

        # For each holder: encapsulate + encrypt master_K with derived key
        encrypted_keys = []
        for holder in data_holders:
            kem = oqs.KeyEncapsulation("ML-KEM-768")
            ciphertext, shared_secret_si = kem.encap_secret(holder["kem_public_key"])

            # Derive AES-256 key from shared_secret_si
            aes_key = hashlib.sha256(shared_secret_si).digest()

            # Encrypt master_K with AES-GCM
            aesgcm = AESGCM(aes_key)
            nonce = os.urandom(12)  # GCM recommended nonce size
            ct = aesgcm.encrypt(nonce, master_K, None)  # no AAD

            encrypted_keys.append({
                "holder_name": holder["name"],
                "kem_ciphertext_base64": base64.b64encode(ciphertext).decode("utf-8"),
                "nonce_base64": base64.b64encode(nonce).decode("utf-8"),
                "encrypted_master_k_base64": base64.b64encode(ct).decode("utf-8")
            })

        # Build payload and sign
        issued_at = datetime.now(timezone.utc)
        valid_until = issued_at + relativedelta(years=validity_years)

        permit_payload = {
            "permit_id": permit_id,
            "issued_at": issued_at.isoformat(timespec="seconds"),
            "valid_until": valid_until.isoformat(timespec="seconds"),
            "domain": domain,
            "encrypted_keys": encrypted_keys
        }

        print(">>>>>> Permit payload (before signing):")
        print(json.dumps(permit_payload, indent=2))

        payload_json = json.dumps(permit_payload, sort_keys=True, separators=(',', ':')).encode("utf-8")
        signature = self.sig.sign(payload_json)

        signed_permit = {
            "payload": payload_json.decode("utf-8"),
            "signature_base64": base64.b64encode(signature).decode("utf-8"),
            "issuer_verification_key_base64": base64.b64encode(issuer_public_key).decode("utf-8")
        }

        result = {"signed_permit_json": json.dumps(signed_permit, indent=2).encode("utf-8")}

        if include_raw_k:
            result["shared_secret_K"] = master_K

        return result