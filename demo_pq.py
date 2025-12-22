# demo_pq.py quantum proof
from utils import generate_ml_kem_keypair, generate_ml_dsa_keypair
from data_permit_issuer import DataPermitIssuer
from data_holder import DataHolder

if __name__ == "__main__":
    # Generate keys
    issuer_keys = generate_ml_dsa_keypair()  # {"public_key", "secret_key"}
    holder1_kem = generate_ml_kem_keypair()
    holder2_kem = generate_ml_kem_keypair()

    # Issuer
    issuer = DataPermitIssuer(issuer_keys["secret_key"])

    result = issuer.issue_data_permit(
        permit_id="HDAB-NL-2025-001",
        domain="scientific-research",
        data_holders=[
            {"name": "DataholderA", "kem_public_key": holder1_kem["public_key"]},
            {"name": "DataholderB", "kem_public_key": holder2_kem["public_key"]}
        ],
        issuer_public_key=issuer_keys["public_key"],  # pass it explicitly
        validity_years=1,
        include_raw_k=True
    )

    signed_permit_json = result["signed_permit_json"]
    print("Post-Quantum Signed Data Permit:")
    print(signed_permit_json.decode("utf-8"))

    # Holders
    holderA = DataHolder("DataholderA", holder1_kem["secret_key"])
    holderB = DataHolder("DataholderB", holder2_kem["secret_key"])

    patient_id = "170401314"
    pseudoA = holderA.process_permit_and_pseudonymize(signed_permit_json, [patient_id])[0]
    pseudoB = holderB.process_permit_and_pseudonymize(signed_permit_json, [patient_id])[0]

    print("\nPseudonym A:", pseudoA)
    print("Pseudonym B:", pseudoB)
    print("Match:", pseudoA == pseudoB)