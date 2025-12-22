# demo.py rsa based implementation
import os
import json
import hashlib
import hmac
import base64
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from typing import Dict, List

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# -----------------------------
# Utility Functions
# -----------------------------
def generate_rsa_keypair() -> Dict:
    """Generate a new RSA key pair (private + public PEM)."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return {"private_pem": private_pem, "public_pem": public_pem}


def load_public_key(pem_bytes: bytes):
    return serialization.load_pem_public_key(pem_bytes)


def load_private_key(pem_bytes: bytes):
    return serialization.load_pem_private_key(pem_bytes, password=None)


# -----------------------------
# HDAB-NL: Issue Signed Data Permit
# -----------------------------
class HDAB_NL:
    def __init__(self, hdab_private_key_pem: bytes):
        self.private_key = load_private_key(hdab_private_key_pem)
        self.public_key = self.private_key.public_key()
        self.public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def issue_data_permit(
        self,
        permit_id: str,
        domain: str,
        data_holders: List[Dict[str, bytes]],
        validity_years: int = 1,
        include_raw_k: bool = False  # ONLY for testing/simulation
    ) -> Dict:
        """
        Generate and sign a data permit.
        Returns a signed permit (JSON-serializable dict).
        """
        # 1. Generate shared secret K (256-bit)
        K = os.urandom(32)

        # 2. Encrypt K for each data holder
        encrypted_keys = []
        for holder in data_holders:
            public_key = load_public_key(holder["public_pem"])
            encrypted_K = public_key.encrypt(
                K,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            encrypted_keys.append({
                "holder_name": holder["name"],
                "encrypted_K_base64": base64.b64encode(encrypted_K).decode("utf-8")
            })

        # 3. Timestamps
        issued_at = datetime.now(timezone.utc)
        valid_until = issued_at + relativedelta(years=validity_years)

        # 4. Build canonical payload (deterministic JSON)
        permit_payload = {
            "permit_id": permit_id,
            "issued_at": issued_at.isoformat(timespec="seconds"),
            "valid_until": valid_until.isoformat(timespec="seconds"),
            "domain": domain,
            "encrypted_keys": encrypted_keys
        }

        # Canonical JSON string (no pretty-print, sorted keys)
        payload_json = json.dumps(permit_payload, sort_keys=True, separators=(',', ':')).encode("utf-8")

        # 5. Sign the payload with RSA-PSS-SHA256
        signature = self.private_key.sign(
            payload_json,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # 6. Assemble signed permit
        signed_permit = {
            "payload": payload_json.decode("utf-8"),  # store as string for easy transmission
            "signature_base64": base64.b64encode(signature).decode("utf-8"),
            "issuer_public_pem": self.public_pem.decode("utf-8")
        }

        result = {"signed_permit_json": json.dumps(signed_permit, indent=2).encode("utf-8")}

        if include_raw_k:
            result["shared_secret_K"] = K  # Only for simulation/testing

        return result


# -----------------------------
# Data Holder: Verify & Process Signed Permit
# -----------------------------
class DataHolder:
    def __init__(self, name: str, private_key_pem: bytes):
        self.name = name
        self.private_key = load_private_key(private_key_pem)

    def _verify_signed_permit(self, signed_permit: Dict) -> Dict:
        """Verify signature and return the parsed payload."""
        payload_str = signed_permit["payload"]
        payload_bytes = payload_str.encode("utf-8")
        signature_b64 = signed_permit["signature_base64"]
        issuer_public_pem = signed_permit["issuer_public_pem"].encode("utf-8")

        signature = base64.b64decode(signature_b64)
        issuer_public_key = load_public_key(issuer_public_pem)

        try:
            issuer_public_key.verify(
                signature,
                payload_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except Exception as e:
            raise ValueError("Invalid signature on permit") from e

        return json.loads(payload_str)

    def extract_shared_secret(self, permit_payload: Dict) -> bytes:
        for entry in permit_payload["encrypted_keys"]:
            if entry["holder_name"] == self.name:
                encrypted_K = base64.b64decode(entry["encrypted_K_base64"])
                K = self.private_key.decrypt(
                    encrypted_K,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                return K
        raise ValueError(f"No encrypted key found for holder {self.name}")

    def pseudonymize_identifier(self, identifier: str, domain: str, K: bytes) -> str:
        message = (identifier + domain).encode("utf-8")
        return hmac.new(K, message, hashlib.sha256).hexdigest()

    def process_permit_and_pseudonymize(
        self,
        signed_permit_json: bytes,
        identifiers: List[str]
    ) -> List[str]:
        """Full flow: verify → check expiry → extract K → pseudonymize."""
        signed_permit = json.loads(signed_permit_json.decode("utf-8"))
        permit_payload = self._verify_signed_permit(signed_permit)

        # Check expiration
        valid_until = datetime.fromisoformat(permit_payload["valid_until"])
        if valid_until < datetime.now(timezone.utc):
            raise ValueError("Permit expired")

        K = self.extract_shared_secret(permit_payload)
        domain = permit_payload["domain"]

        return [self.pseudonymize_identifier(id_, domain, K) for id_ in identifiers]


# -----------------------------
# Example Usage / Simulation
# -----------------------------
if __name__ == "__main__":
    # Generate key pairs
    hdab_keys = generate_rsa_keypair()
    holder1_keys = generate_rsa_keypair()
    holder2_keys = generate_rsa_keypair()

    # HDAB-NL issues a signed permit
    hdab = HDAB_NL(hdab_keys["private_pem"])

    result = hdab.issue_data_permit(
        permit_id="HDABNL-2025-723",
        domain="scientific-research",
        data_holders=[
            {"name": "DataholderA", "public_pem": holder1_keys["public_pem"]},
            {"name": "DataholderB", "public_pem": holder2_keys["public_pem"]}
        ],
        validity_years=1,
        include_raw_k=True  # Only for demo
    )

    signed_permit_json = result["signed_permit_json"]
    print("Signed Data Permit issued:")
    print(signed_permit_json.decode("utf-8"))

    # Data holders process the signed permit
    holderA = DataHolder("DataholderA", holder1_keys["private_pem"])
    holderB = DataHolder("DataholderB", holder2_keys["private_pem"])

    patient_bsn = "170401314"

    pseudoA = holderA.process_permit_and_pseudonymize(signed_permit_json, [patient_bsn])[0]
    pseudoB = holderB.process_permit_and_pseudonymize(signed_permit_json, [patient_bsn])[0]

    print("\nPseudonym generated by DataholderA:", pseudoA)
    print("Pseudonym generated by DataholderB:", pseudoB)
    print("Match (deterministic linkage possible):", pseudoA == pseudoB)