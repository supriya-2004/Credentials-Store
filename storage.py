import sqlite3
import json
import base64
from abc import ABC, abstractmethod

# Abstract Base Class for all storage types
class Storage(ABC):
    @abstractmethod
    def store_key(self, service_name, encrypted_key, salt):
        pass

    @abstractmethod
    def retrieve_key(self, service_name):
        pass

# 1. In-Memory Storage
class InMemoryStorage(Storage):
    def __init__(self):
        self._credentials = {}
        print("Using In-Memory storage. Data will be lost on exit.")

    def store_key(self, service_name, encrypted_key, salt):
        self._credentials[service_name] = {"key": encrypted_key, "salt": salt}
        print(f"Stored credentials for '{service_name}' in memory.")

    def retrieve_key(self, service_name):
        return self._credentials.get(service_name)

# 2. File Storage
class FileStorage(Storage):
    def __init__(self, filename="credentials.json"):
        self._filename = filename
        self._credentials = self._load_from_file()
        print(f"Using File storage ('{self._filename}').")

    def _load_from_file(self):
        try:
            with open(self._filename, 'r') as f:
                encoded_data = json.load(f)
                # Decode from Base64 back to bytes
                decoded_data = {}
                for service, data in encoded_data.items():
                    decoded_data[service] = {
                        "key": base64.b64decode(data["key"]),
                        "salt": base64.b64decode(data["salt"])
                    }
                return decoded_data
        except FileNotFoundError:
            return {}

    def _save_to_file(self):
        # Encode bytes to Base64 strings for JSON compatibility
        encoded_data = {}
        for service, data in self._credentials.items():
            encoded_data[service] = {
                "key": base64.b64encode(data["key"]).decode('utf-8'),
                "salt": base64.b64encode(data["salt"]).decode('utf-8')
            }
        with open(self._filename, 'w') as f:
            json.dump(encoded_data, f, indent=4)

    def store_key(self, service_name, encrypted_key, salt):
        self._credentials[service_name] = {"key": encrypted_key, "salt": salt}
        self._save_to_file()
        print(f"Stored credentials for '{service_name}' in '{self._filename}'.")

    def retrieve_key(self, service_name):
        return self._credentials.get(service_name)

# 3. Database Storage
class DatabaseStorage(Storage):
    def __init__(self, db_name="credentials.db"):
        self._db_name = db_name
        self._conn = sqlite3.connect(self._db_name)
        self._create_table()
        print(f"Using Database storage ('{self._db_name}').")

    def _create_table(self):
        cursor = self._conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                service_name TEXT PRIMARY KEY,
                encrypted_key BLOB NOT NULL,
                salt BLOB NOT NULL
            )
        ''')
        self._conn.commit()

    def store_key(self, service_name, encrypted_key, salt):
        try:
            cursor = self._conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO credentials (service_name, encrypted_key, salt) VALUES (?, ?, ?)",
                (service_name, encrypted_key, salt)
            )
            self._conn.commit()
            print(f"Stored credentials for '{service_name}' in the database.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def retrieve_key(self, service_name):
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT encrypted_key, salt FROM credentials WHERE service_name = ?",
            (service_name,)
        )
        result = cursor.fetchone()
        if result:
            return {"key": result[0], "salt": result[1]}
        return None

    def __del__(self):
        if self._conn:
            self._conn.close()