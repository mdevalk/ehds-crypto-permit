# A Cryptographic Data Permit Mechanism for Secure Secondary Use of Health Data in the European Health Data Space

###  HDAB-Coordinated, At-Source Pseudonymization Enabling Deterministic Data Linking Across Multiple Data Holders  

---

## Abstract
The European Health Data Space (EHDS) Regulation (EU) 2025/327 establishes a comprehensive framework that enables the secondary use of electronic health data for purposes such as research, innovation, public health, and policymaking, subject to strict privacy and governance safeguards. Under the Regulation, data processed for secondary-use purposes must by default be anonymized, with pseudonymization permitted only when necessary to maintain analytical value—particularly when consistent cross-dataset record linkage is required across data holders at national or EU level.

Traditional secondary-use workflows often rely on centralized pseudonymization services, requiring data holders to transmit identifiable personal data to a trusted intermediary before pseudonymization takes place. This model introduces avoidable privacy and security risks, especially during the transfer of raw identifiers.

This proposal introduces a cryptographic data‑permit–based mechanism that enables pseudonymization directly at source, while still generating deterministic and linkable pseudonyms across all participating data holders. This ensures that reliable record linkage can occur within a Secure Processing Environment (SPE), without raw personal identifiers ever leaving the data holder’s environment, thereby significantly reducing exposure risks while maintaining analytical integrity.

The core innovation lies in the synergistic combination of the following two elements:

- the use of **the data permit as an active cryptographic** mechanism that serves as a secure, auditable authorization and coordination token, and  
- the use of **key wrapping to securely distribute a data-application specific shared secret** to authorized data holders through this permit.

Together, these enable fully decentralized, synchronized pseudonym generation, eliminating the need for raw shared secret transfers while preserving end-to-end privacy and security.

## Introduction
The European Health Data Space (EHDS) Regulation requires each Member State to designate a Health Data Access Body (HDAB) responsible for facilitating the secure secondary use of electronic health data. In the Netherlands, the HDAB-NL programme—led by the Ministry of Health, Welfare and Sport (VWS) in collaboration with Health-RI, RIVM, CBS, and ICTU—is developing the necessary infrastructure, metadata catalogue, data access application management system (DAAMs) and Secure Processing Environments (SPE).

**Key Challenges in multi data-holder Integration**
Linking data from multiple independent data holders while complying with strict EHDS privacy requirements presents several fundamental difficulties:

- **Central pseudonymization**: This approach requires data holders to transfer raw personal identifiers to a trusted third party or place HDAB as data processor, creating significant privacy and security risks during transmission and storage of pseudonym tables
- **at-source pseudonymization**: it produces inconsistent pseudonyms across holders, forcing reliance on probabilistic matching techniques and resulting in reduced linkage quality and analytical utility
- **end-to-end security**: lack of a unified framework for securing key distribution, data exchange, access control, and workflow synchronization across decentralized parties introduces significant complexity and risk
- **lack of a unified exchange and linking mechnanism** that enables secure and compliant national and cross‑border linkage of health datasets in the EU

This proposal directly addresses these challenges. It fully aligns with EHDS data minimisation and privacy-by-design principles by enabling pseudonymization at source with deterministic consistency, thereby maximising privacy protection while preserving high-quality cross-data-holder record linkage.

## The Proposed Solution
The solution introduces a **cryptographic data permit mechanism** in which the HDAB issues a machine-readable, digitally signed permit that serves as both an authorisation token and a secure coordination instrument. Through **key wrapping**, the permit securely distributes a project-specific shared secret to all authorised data holders, enabling them to perform consistent deterministic pseudonymization locally. The resulting pseudonymised datasets are uploaded to designated storage locations, where they can be mounted and linked within a secure processing environment—without raw personal identifiers ever leaving the data holders’ controlled environments. 

This approach eliminates the privacy risks of central identifier transfer, avoids the linkage degradation of uncoordinated pseudonymization, and provides the HDAB with a robust mechanism to orchestrate secure, auditable, and EHDS-compliant multi-holder data linkage. 

The mechanism is equally applicable to **cross-border data linkage**. However, the effectiveness of deterministic pseudonymization for reliable record linkage depends on the availability of uniform or harmonised personal identifiers (e.g., national ID numbers, health insurance IDs, or other stable direct identifiers) across the participating data holders and Member States. In cases where such uniform identifiers are absent or inconsistent, supplementary techniques—such as probabilistic matching or additional privacy-preserving record linkage methods—may be required to achieve sufficient linkage quality.

## Core Concept
The core concept is to transform the data permit into a **cryptographically signed, machine-readable authorization and coordination token**. This active cryptographic instrument enables secure, privacy-preserving secondary use of electronic health data **without ever disclosing raw personal identifiers to third parties** or the data user.

The permit can either complement an existing administrative ('paper') permit or fully integrate its cryptographic functionality into the data permit issued by the HDAB. By embedding securely wrapped shared secrets, storage locations and explicit data linkage instructions, the data permit becomes an **operational cryptographic token**.

Figure 1. depicts a simplified interaction model for the cryptographic data permit mechanism within the EHDS context. It highlights the triangular relationship between the Health Data Access Body (HDAB), the Data Holder, and the Data User, with the data permit serving as the central coordination and authorization token to enable secure data exchange and reliable data linkage.

![Diagram](images/figure1.png)
Figure 1. EHDS data and data-permit exchange

- HDAB (Health Data Access Body), the permit issuing authority, creates and distributes a data permit to **both the data user and the data holder**
- The data holder receives the permit and uses it to **pseudonymize locally** and distrubute the pseudonymized dataset to the authorized storage locations
- The data user receives the permit, which **authorizes access to storage locations** containing the pseudonymized data that can be retrieved for linkage in a Secure Processing Environment (SPE)

A operational cryptographic data permit facilitates:
- secure authentication and authorization of data holders and data users,
- coordinated at-source pseudonymization with deterministic consistency
- controlled provision of pseudonymized datasets to designated storage locations
- reliable record linkage across multiple pseudonymized datasets within a SPE

> This approach guarantees end-to-end security while equipping the Health Data Access Body (HDAB) with a robust, auditable mechanism to coordinate compliant, multi-holder, and cross-border data access.

## Detailed Solution Description

### Mechanism Overview
![Diagram](images/figure2.png)
Figure 2. Mechanism Overview

1. The HDAB issues a digitally signed data permit to the **data user**, and **all data holders** involved in a certain data application (data request or data access application)
2. Data holders **validate the authenticity** of the permit by verifing the signature of the permit
3. Data holders **unwrap the shared secret**, with their own private key
4. Data holders perform **local pseudonymization** on the requested dataset based on the shared secret
5. Data holders place the pseudonymized dataset on the **specific storage location** as indicated by the permit
6. In the SPE, the authenticated data user uploads the permit, ingests the pseudonymized datasets from the storage locations indicated in the permit and and **links the datasets** based on the pseudonomized records
7. The linked dataset is **available for analysis**
- Once the research is completed, output control can be carried out by the output controller as indicated in the permit

### Design principles
- a machine-readable data permit is used an operational document in the workflow
- the permit is shared with both the data holder and the data user
- SPE functionality and storage are regarded as separate concerns decoupling functionality and data storage
- The permit contains all information necessary for all participants to prepare, exchange, and link the datasets and to conduct and conclude the research
- pseudonymization is done by the dataholders

### Key Benefits
- Maximum Privacy Protection: Raw personal data remains confined to the data holder's premises, eliminating the risks associated with centralised identifier transfers
- High-Quality Record Linkage: Deterministic pseudonyms allow precise cross-data-holder and cross-border linkage in secure processing environments, preserving essential analytical utility
- Future-Proof Design: Post-quantum readiness for ML-KEM key encapsulation and ML-DSA signing
- facilitates cross-border data sharing across the EU by allowing a unified, secure and privacy-preserving linkage of data from multiple holders across member states
- Full EHDS Compliance: the approach aligns with the Regulation's emphasis on data minimisation, pseudonymization only when necessary (as justified for linkage under relevant provisions, including Recital 72 on early de-identification), and strong technical safeguards

## Permit issuance
The data permit is issued after the HDAB completes its review and approves the data application. At this stage, the HDAB assembles the identities of all authorised data users and data holders, the datasets to be accessed, the linkage method to be used, and the encrypted shared secrets needed for secure processing. These elements are then consolidated into a signed, machine‑readable permit object (see Figure 3), typically represented in a structured format such as JSON.

![Diagram](images/figure3.png)
Figure 3. Data permit object

Data permit attributes:
- **permitId** is the unique identifier given to the permit by the issuing HDAB
- **dataUsers** list of authorized data users
- **dataHolders** list of data holder's id's (and potentially public keys to enable central key wrapping)
- **datasetId** list of the identifiers of the datasets involved in this data application
- **analysisMethod** the analysis and linking method used in for this data application deterministric-pseudonymization.
- **sharedSecrets** list of shared secret, encrypted per dataholder
- **outputController** identity of the designated output controller
- **signature** added to the permit by the issuing HDAB for verification by the data holders and validated at the issuing certificate authority

> **Note:** Above permit only shows attributes relavant for demonstrating the mechanism, full sample permit available in [sample_permit.json](sample_permit.json)

### Identity management
Data holders generate a keypair in advance, preferably using an eIDAS‑compatible or national public key infrastructure (PKI), and register their public keys with the HDAB (DAAMs system), enabling these keys to be used during the permit process. The data holders’ public keys are subsequently used for operations such as securely wrapping the shared secret.

Data users make use of an eIDAS-compatible identity. These keys are used to determine their identity, authenticate access requests, and, where applicable, to verify authorisations and signatures associated with issued permits. All registered keys must be issued or certified by a trusted certificate authority recognised by the HDAB. Key lifecycle management is governed by the applicable PKI policies and is enforced by the HDAB.

### Authorization
The data permit explicitly defines and enables the following authorisations:
- Write access for data holders: Each authorised data holder receives temporary, scoped write permissions to the specific storage location(s) indicated in the permit for their dataset(s). This allows them to upload the locally pseudonymised dataset after processing, while preventing read access to other holders’ data or unrelated locations.
- Read access for data users in the SPE: Authenticated data users (researchers) are granted read-only access to all relevant storage locations, but only within the secure processing environment. The SPE mounts these locations based on the validated permit, ensuring that data ingestion occurs in an isolated, controlled setting with no possibility of exfiltration of raw or pseudonymised data outside the SPE.
- No direct access outside the workflow: Neither data holders nor data users can access the storage locations outside the permit-defined context. Permissions are time-bound (aligned with the permit’s validity period) and purpose-specific, automatically revoked upon expiry or completion of the application.
- Auditable and revocable: All access grants are traceable to the signed permit, enabling the HDAB to monitor compliance and revoke permissions if necessary

### Key exchange
- **'Permit Issuer' (HDAB) public key** The permit includes the HDAB’s public key to enable participants to verify the HDAB’s digital signature on the permit itself. In this proof-of-concept implementation, the full public key is embedded directly in the permit for simplicity and immediate usability. In production deployments, data holders and SPEs should validate the HDAB’s signing certificate against a trusted national or eIDAS-qualified certificate authority, eliminating the need to embed the key and allowing standard revocation checking (CRL/OCSP)
- **'Data Holder' Public Keys** Each authorised data holder registers a certified public key (e.g., RSA-2048/3072 or post-quantum equivalent) with the HDAB in advance.
These public keys are included in the permit within the structured dataHolders array
- **'Data User' Identities** The identities of authorised data users are explicitly listed in the permit under the dataUsers field. Each entry includes a strong, verifiable identifier (preferably an eIDAS-qualified electronic identification or a national researcher registry URN), along with optional human-readable attributes such as name, organisation, and role.
These identities serve as the basis for authentication and access control within the SPE.

### Key wrapping
In order to be able to share the pseudonymization key across data holders, the designated HDAB generates a random shared secret `K`, specific for each data application. For each authorized holder `DHᵢ` the shared secret `K` is encrypted so that only that specific data holder is able to decrypt a single shared secret. This means that for a data application with multiple dataholders the wrapped shared secret appears multiple times in in the permit, each wrapped for a specific dataholder.

   ```text
   wrappedSecretᵢ = PK-Encrypt(PubKeyᵢ, K)
   ```

Demos included, RSA: [demo_rsa.py](demo_rsa.py), Post Quantum KEM/DSA: [demo_pq.py](demo_pq.py)

## Pseudonymization at source
Once the permit is issued, the permit is distributed to both the data holders and data users. Each data holder verifies the HDAB signature, and decrypts its wrapped instance of shared secret K, and performs pseudonymization according to the instreuctions, as defined in the permit. There is no reason for the data holder to store the shared secret since it it can be directly derived from the permit. 

Subsequently the pseudonomized dataset is stored at the storage location for the specific dataset, as indicated in the permit. Authorization on the storage locations is managed by the HDAB. 

### Storage locations
The cryptographic data permit explicitly designates storage locations for the pseudonymised datasets contributed by each data holder. These locations—typically access-controlled object storage buckets (e.g., S3-compatible endpoints) or equivalent cloud-based storage services—act as secure, neutral intermediaries between data holders and the secure processing environment. The storage location type can be indicated in the permit to enable different HDABs and memberstates to uses different storage types.


## Record linkage
The data user is granted access to the SPE by the HDAB using its eIDAS identity. In the SPE the data user is able to ingest data datasets in the SPE, by combining the data permit with its eIDAS identity. 

A secure HDAB software component, running in the SPE accepts and validates the permit, authenticates the  authorized data users, accesses the storage locations and ingest and links the datasets in the SPE.

Data linkage is performed according to the method indicated in the permit, and the combined dataset is created in the SPE. The data user is able to conduct the research and signal output control and completion to the HDAB.

The plug‑in architecture of the HDAB software component enables SPE operators to extend their existing SPE offerings in order to meet EHDS complicance. The HDAB component is installed jsut like other specific tool installations in the SPE.


## Extensibility
This mechanism can be extended to support other privacy-preserving analysis methods beyond deterministic pseudonymization. By incorporating an extensible analysisMode field in the permit, future modes—such as secure multi-party computation (MPC), federated learning, and federated analytics—can be enabled by guiding data holders on how to prepare the data. In all cases, the same cryptographic data permit functions as the coordination and authorization mechanism.

## Conclusion
The cryptographic data permit mechanism presented in this whitepaper offers a robust, privacy-enhancing solution for the secure secondary use of electronic health data within the European Health Data Space (EHDS). By transforming the conventional data permit into an active cryptographic instrument, it enables at-source pseudonymization with deterministic consistency across multiple data holders, ensuring that raw personal identifiers never leave the controlled environment of the data holder.

This mechanism can serve as a unified protocol for cross-border data sharing across EU Member States, allowing diverse data holders to link and analyze data securely and consistently, fully aligned with EHDS principles and regulatory requirements.

## References
- [ehds-crypto-permit](https://github.com/mdevalk/ehds-crypto-permit) – Minimal Proof-of-Concept repository demonstrating permit issuance and data holder functionality.
- [European Health Data Space (EHDS)](https://health.ec.europa.eu/ehealth-digital-health-and-care/european-health-data-space_en) – Official information on the EHDS initiative
- [Open Quantum Safe](https://openquantumsafe.org/) – Open Quantum Safe project
