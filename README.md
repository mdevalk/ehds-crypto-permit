# A Cryptographic Data Permit Mechanism for Secure Secondary Use of Health Data in the European Health Data Space (EHDS)

[![EHDS Proposal](https://img.shields.io/badge/EHDS-Proposal-blue)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32025R0327)
[![Whitepaper](https://img.shields.io/badge/View-Whitepaper-blue?logo=github)](WHITEPAPER.md)
[![Privacy by Design](https://img.shields.io/badge/Privacy-by%20Design-green)](https://gdpr.eu/privacy-by-design/)
[![Post-Quantum Ready](https://img.shields.io/badge/Post--Quantum-Ready-orange)](https://csrc.nist.gov/projects/post-quantum-cryptography)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)


## Introduction

This repository contains a proof-of-concept implementation of a **cryptographic data-permit mechanism** for secure data exchange and pseudonymization across data-holder environments governed by a Health Data Access Body (HDAB), in line with the European Health Data Space (EHDS) Regulation (EU) 2025/327.

The mechanism transforms the EHDS data permit issued by a Health Data Access Body (HDAB) into an **active cryptographic coordination token**, enabling secure exchange and combination of healthdata from different sources while keeping personal identifiers (ie. BSN (the Dutch Citizen Service Number)) decentralized at the data holders.

This proof-of-concept code is accompanied by a detailed whitepaper that describes the full protocol design, security considerations, EHDS compliance rationale, and potential extensions for additional analysis modes.

## Whitepaper

[A Cryptographic Data Permit Mechanism for Secure Secondary Use of Health Data in the European Health Data Space](WHITEPAPER.md)

## Quick Start

```bash

# liboqs may need to be built from source
./install_oqs.sh

# Install dependencies
pip install -r requirements.txt

# Classic RSA Demo (deterministic pseudonymization)
python demo.py

# Post-Quantum Demo (deterministic pseudonymization)
python demo_pq.py
```

## Repository Overview

```text
ehds-crypto-permit/
├── data_permit_issuer.py  # Minimal permit issuer (HDAB)
├── data_holder.py         # Minimal data Holder
├── utils.py               # Utility functions keypair generation 
├── demo_rsa.py            # PoC demo using on RSA
└── demo_pq.py             # PoC demo based on KEM/DSA (post-quantum)
```