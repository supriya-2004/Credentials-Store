# Credentials Store - API Key Manager

A simple, command-line tool designed to securely store and retrieve API keys for various services. This program uses strong encryption and offers multiple storage backends to manage your credentials safely and efficiently.

---

## 🧩 Features
- **Master Password Protection**: All your credentials are secured behind a single master password for the session.
- **Strong Encryption**: API keys are never stored in plaintext. We use AES encryption provided by the `cryptography` library.
- **Secure Key Derivation**: A robust encryption key is derived from your master password using **PBK-DF2-HMAC** with a high iteration count.
- **Individual Salting**: Each stored secret is individually salted to protect against pre-computation attacks like rainbow tables.
- **Multiple Storage Backends**: Choose the storage method that fits your needs, namely, **In-Memory, Encrypted JSON File and SQLite Database**.


