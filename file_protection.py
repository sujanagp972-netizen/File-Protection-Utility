from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"


def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as file:
            file.write(key)


def load_key():
    with open(KEY_FILE, "rb") as file:
        return file.read()


def protect_file():
    filename = input("Enter the file name to protect: ")

    if not os.path.exists(filename):
        print("File not found.")
        return

    key = load_key()
    cipher = Fernet(key)

    with open(filename, "rb") as file:
        data = file.read()

    protected_data = cipher.encrypt(data)

    with open(filename + ".protected", "wb") as file:
        file.write(protected_data)

    print("File protected successfully.")


def restore_file():
    filename = input("Enter the protected file name: ")

    if not os.path.exists(filename):
        print("File not found.")
        return

    key = load_key()
    cipher = Fernet(key)

    with open(filename, "rb") as file:
        protected_data = file.read()

    try:
        original_data = cipher.decrypt(protected_data)
    except Exception:
        print("Unable to restore file. The key may be incorrect or the file may be damaged.")
        return

    output_file = filename.replace(".protected", "_restored")

    with open(output_file, "wb") as file:
        file.write(original_data)

    print("File restored successfully.")


generate_key()

print("\n--- File Protection Utility ---")
print("1. Protect File")
print("2. Restore File")

choice = input("Enter your choice: ")

if choice == "1":
    protect_file()
elif choice == "2":
    restore_file()
else:
    print("Invalid choice.")