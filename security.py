import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a cryptographic key from a password and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000, # A high iteration count for security
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_key(api_key: str, master_password: str) -> (bytes, bytes):
    """Encrypts an API key and returns the encrypted data and salt."""
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    f = Fernet(key)
    encrypted_api_key = f.encrypt(api_key.encode())
    return encrypted_api_key, salt

def decrypt_key(encrypted_api_key: bytes, salt: bytes, master_password: str) -> str:
    """Decrypts an API key using the master password and salt."""
    key = derive_key(master_password, salt)
    f = Fernet(key)
    try:
        decrypted_api_key = f.decrypt(encrypted_api_key).decode()
        return decrypted_api_key
    except Exception:
        # This will fail if the master password is wrong
        return None