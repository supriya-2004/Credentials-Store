# Credentials Store - API Key Manager

A simple, command-line tool designed to securely store and retrieve API keys for various services. This program uses strong encryption and offers multiple storage backends to manage your credentials safely and efficiently.

---

## 🧩 Features
- **Master Password Protection**: All your credentials are secured behind a single master password for the session.
- **Strong Encryption**: API keys are never stored in plaintext. We use AES encryption provided by the `cryptography` library.
- **Secure Key Derivation**: A robust encryption key is derived from your master password using **PBK-DF2-HMAC** with a high iteration count.
- **Individual Salting**: Each stored secret is individually salted to protect against pre-computation attacks like rainbow tables.
- **Multiple Storage Backends**: Choose the storage method that fits your needs, namely, **In-Memory, Encrypted JSON File and SQLite Database**.

---

## 🛠️ Technology Stack 
- Language: Python 3
- Core Library: `cryptography` for all cryptographic operations.
```bash
pip install cryptography
```
---

## How to Use the Program ▶️
1. Run the Application
Execute the main script from your terminal:
```bash
python main.py
```
2. Enter Master Password
You will be prompted to enter a master password. This password will be used to encrypt and decrypt your keys for the current session.
```bash
--- API Key Storage System ---
Please enter your master password: ********
```
3. Choose a Storage Method
Select how you want to store your credentials for this session.
```bash
Choose a storage method:
1. In-Memory (data is lost on exit)
2. File (data is saved to credentials.json)
3. Database (data is saved to credentials.db)
Enter your choice (1/2/3): 2
```
4. Select an Action
Choose whether you want to store a new key or retrieve an existing one.
```bash
What would you like to do?
1. Store a new API key
2. Retrieve an API key
3. Exit
Enter your choice (1/2/3): 1
```
5. Follow the Prompts

- **To Store**: Provide the service name (e.g., 'GitHub') and the API key.

- **To Retrieve**: Provide the service name you want the key for. The retrieved key will be printed to the console.

---

## Project Structure 📁
The project is organized into three main modules for a clean separation of concerns:

- `main.py`: The application's entry point. Handles the command-line user interface and orchestrates the overall flow.

- `security.py`: Manages all cryptographic operations, including key derivation, encryption, and decryption.

- `storage.py`: Defines the storage logic. It contains a base Storage class and its implementations: `InMemoryStorage`, `FileStorage` and `DatabaseStorage`.

- `credentials.json`: (Generated) The default file created by `FileStorage`.

- `credentials.db`: (Generated) The default database created by `DatabaseStorage`.

---

## Conclusion

This project successfully demonstrates how to build a secure and modular command-line application for managing sensitive credentials like API keys. By prioritizing security and flexibility, the system provides a reliable solution to the common problem of storing secrets.

