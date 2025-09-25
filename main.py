import getpass
from storage import InMemoryStorage, FileStorage, DatabaseStorage
from security import encrypt_key, decrypt_key

def get_storage_handler():
    """Asks the user to choose a storage method and returns an instance."""
    print("\nChoose a storage method:")
    print("1. In-Memory (data is lost on exit)")
    print("2. File (data is saved to credentials.json)")
    print("3. Database (data is saved to credentials.db)")

    while True:
        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
            return InMemoryStorage()
        elif choice == '2':
            return FileStorage()
        elif choice == '3':
            return DatabaseStorage()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    print("--- API Key Storage System ---")
    master_password = getpass.getpass("Please enter your master password: ")

    storage_handler = get_storage_handler()

    while True:
        print("\nWhat would you like to do?")
        print("1. Store a new API key")
        print("2. Retrieve an API key")
        print("3. Exit")
        action = input("Enter your choice (1/2/3): ")

        if action == '1':
            service_name = input("Enter the service name (e.g., 'OpenAI'): ")
            api_key = getpass.getpass(f"Enter the API key for {service_name}: ")
            
            encrypted_key, salt = encrypt_key(api_key, master_password)
            storage_handler.store_key(service_name, encrypted_key, salt)

        elif action == '2':
            service_name = input("Enter the service name to retrieve: ")
            data = storage_handler.retrieve_key(service_name)
            
            if data:
                decrypted_key = decrypt_key(data["key"], data["salt"], master_password)
                if decrypted_key:
                    print(f"\nAPI Key for '{service_name}': {decrypted_key}")
                else:
                    print("\n[Error] Failed to decrypt key. Master password may be incorrect.")
            else:
                print(f"\nNo API key found for '{service_name}'.")

        elif action == '3':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()