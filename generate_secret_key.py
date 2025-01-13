import os
import secrets

SECRET_KEY_FILE = "secret.key"

def generate_secret_key():
    if not os.path.exists(SECRET_KEY_FILE):
        secret_key = secrets.token_hex(32)
        with open(SECRET_KEY_FILE, "w") as f:
            f.write(secret_key)
        print(f"Secret key generated and saved to '{SECRET_KEY_FILE}'.")
    else:
        print(f"Secret key already exists in '{SECRET_KEY_FILE}'.")

if __name__ == "__main__":
    generate_secret_key()
