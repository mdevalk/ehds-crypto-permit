## A Cryptographic Data Permit Mechanism for Secure Secondary Use of Health Data in the European Health Data Space

#### A Privacy-Enhancing Proposal the European Health Data Space (EHDS) originally defined for the Dutch Health Data Access Body (HDAB-NL)
---

### Abstract
The European Health Data Space (EHDS) Regulation (EU) 2025/327 enables secondary use of electronic health data while prioritizing privacy. By default, data must be anonymized; pseudonymization is allowed only when necessary to preserve utility, particularly for linking records across multiple datasets on national level and across european member states.

Traditional approaches rely on central pseudonymization, requiring data holders (DH) to transmit identifiable data to a central party, which introduces significant privacy risks during transfer.

This proposal introduces a cryptographic data permit mechanism enabling pseudonymization at source with consistent, deterministic pseudonyms across all holders. This allows record linking across multiple datasets in a single Secure Processing Environment (SPE) without raw identifiers ever leaving the data holder's premises**.

The core innovation is key wrapping: an application-specific shared secret is securely distributed to authorized data holders via a **cryptographic data permit**, enabling decentralized yet consistently synchronized pseudonym generation.

### Introduction
The EHDS requires each Member State to designate a HDAB organization to facilitate secondary use of health data. In the Netherlands, the **HDAB-NL program**—led by the Ministry of Health, Welfare and Sport (VWS) with Health-RI, RIVM, CBS, and ICTU—is building infrastructure, governance, a DAAMs, a metadata catalog, and Secure Processing Environments.

#### Key Challenges with multi data holder data integration
- **Central pseudonymization**: Requires transfer of raw identifiers, introducing postential privacy and security risks.  
- **Independent at-source pseudonymization**: Results in inconsistent pseudonyms → reliance on fuzzy matching → reduced linkage quality.
- Coordination of key- and data exchange, end-to-end security
This proposal aligns with EHDS data minimization principles, maximizing privacy while preserving high-quality data linkage.

The proposed solution...

### Core Concept
The core idea is to use the **data permit as a cryptographically signed authorization and coordination token** that enables secure, privacy-preserving secondary use of health data **without the need to disclose personal identifiers**. This permit could be additional to the 'paper' permit or can be embedded in the permit.

The data permit acts as an machine-readable **active cryptographic mechanism** that enables secure data exchange, authorizations and record linkage across datasets.

### Permit Mechanism Description
![Diagram](images/figure1.png)
Figure 1. Mechanism Overview

1. The HDAB issues a digitally signed data permit to the **data user**, and **all data holders** involved in a certain data application (data request or data access application)
2. Data holders **validate the authenticity** of the permit by verifing the signature of the permit
3. Data holders **unwrap the shared secret**, with their own private key
4. Data holders perform **local pseudonymization** on the requested dataset based on the shared secret
5. Data holders place the pseudonymized dataset on the **specific storage location** as indicated by the permit
6. In the SPE, the authenticated data user uploads the permit, ingests the pseudonymized datasets on storage locations indicated in the permit and and **links the datasets** based on the pseudonomized records
7. The linked dataset is **available for analysis**

Additionally
The research result can be made available in a dedicated storage location (indicated in the permit) for an output controller to be checked using a separate SPE, specifically for this purpose, without risk on exposing the linked dataset to the controller.

### Detailed Solution Description


#### Permit

![Diagram](images/figure2.png)
Figure 2. Data permit object attributes

- **permitId** is the unique identifier given to the permit by the issuing HDAB
- **dataUsers** list of authorized data users
- **dataHolders** list of data holder's id's (and potentially public keys to enable central key wrapping)
- **datasetId** list of the identifiers of the datasets involved in this data application
- **analysisMethod** the analysis and linking method used in for this data application deterministric-pseudonymization.
- **sharedSecrets** list of shared secret, encrypted per dataholder
- **outputController** identity of the designated output controller
- **signature** added to the permit by the issuing HDAB for verification by the data holders and validated at the issuing certificate authority

> **Note:** Above permit only shows attributes relavant for demonstrating the mechanism, full sample permit available in [sample_permit.json](sample_permit.json) 

#### Identities
- Data holders generate a keypair upfront and register certified public keys with the HDAB (leveraging eIDAS-compatible infrastructure or national PKI infrastructure)
- data users use an eIDAS-compatible identity

#### Authorization
- **authorization** on the storage locations for the participants of the data application, typically data holders to be able to store the pseudonomized data sets and for the data user to be access the data sets in the storage locations.

#### Key exchange
- HDAB public key
For simplicity, in the current implementation, the public key of the HDAB is added to the permit. The certificate is to be validated at the issuing certificate authority.
- Public keys of Data holders are added to the permit in the list of data holders together with an index so that the certificate can be ascociated with the dataset id and storage location

#### Key wrapping
In order to be able to share the pseudonymization key across data holders:
1. HDAB generates a random shared secret `K` scoped to the project (and potentially validity period).  
2. For each authorized holder `DHᵢ` the shared secret K is encrypted so that only that specific data holder is able to decrypt a single shared secret. This means that for a data application with 3 dataholders the shared secret is available three times, for all data holder but encrypted with the public key of the specific dataholder.

   ```text
   wrappedSecretᵢ = PK-Encrypt(PubKeyᵢ, K)
   ```

##### storage locations



### Key Benefits
- Raw personal data never leaves the data holder’s environment  
- Deterministic linkage across multiple holders  
- Full EHDS compliance (Recital 72, Article 33)  
- Post-quantum ready: Supports ML-KEM for key encapsulation and ML-DSA for signing  
- Extendable by design via `analysis_mode`. Currenlty on deterministric pseudonymization but the mechanism allows for future processing types like multi-party computation, federated analytics and federated learning

### Features / implementation choices
- Classic RSA mode: RSA-OAEP key transport + RSA-PSS signing  
- Post-quantum mode: ML-KEM-768 + AES-GCM wrapping + ML-DSA-65 signing  
- Deterministic pseudonymization via HMAC-SHA256 
- Time-bound, domain-scoped, purpose-specific permits  
- Canonical JSON payload, digitally signed by the issuing HDAB  
- Modular, pure-Python, well-documented, extensible code  
- the pseudonyms enable anonynization of the records which relation to patients can be made by the dataholders   

#### Technology / implementation choices
- based on asymetric cryptography
- peer-to-peer API based model
- no propriatary networks required
- the data itself is encrypted as well as the transport and while at rest