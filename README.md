# A Cryptographic Data Permit Mechanism for Secure Secondary Use of Health Data in the European Health Data Space

[![EHDS Proposal](https://img.shields.io/badge/EHDS-Proposal-blue)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32025R0327)
[![Whitepaper](https://img.shields.io/badge/View-Whitepaper-blue?logo=github)](WHITEPAPER.md)
[![Privacy by Design](https://img.shields.io/badge/Privacy-by%20Design-green)](https://gdpr.eu/privacy-by-design/)
[![Post-Quantum Ready](https://img.shields.io/badge/Post--Quantum-Ready-orange)](https://csrc.nist.gov/projects/post-quantum-cryptography)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)


### Overview

This repository contains a proof-of-concept implementation of a **cryptographic data-permit mechanism** for secure data exchange and pseudonymization across data-holder environments governed by a Health Data Access Body (HDAB), in line with the European Health Data Space (EHDS) Regulation (EU) 2025/327.

The mechanism transforms the standard EHDS data permit into an **active cryptographic coordination token**, enabling secure exchange and combination of health from different sources while keeping personal identifiers (like BSN, the Dutch Citizen Service Number) decentralized at the data holders.

This proof-of-concept repository is accompanied by a detailed whitepaper that describes the full protocol design, security considerations, EHDS compliance rationale, threat model, and planned extensions for advanced privacy-preserving analysis modes. 

**A Cryptographic Data Permit Mechanism for Secure Secondary Use of Health Data in the European Health Data Space**  
December 2025

[Read the whitepaper here](WHITEPAPER.md)

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Classical RSA Demo (deterministic distributed pseudonymization)
python demo.py

# Post-Quantum Demo (deterministic distributed pseudonymization)
python demo_pq.py
```