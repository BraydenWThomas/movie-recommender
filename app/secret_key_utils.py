import os
import secrets

SECRET_KEY_FILE = "secret.key"

def generate_secret_key():
    """Generate a strong secret key and save it to a file."""
    if not os.path.exists(SECRET_KEY_FILE):
        secret_key = secrets.token_hex(32)  # Generates a 64-character hexadecimal string
        with open(SECRET_KEY_FILE, "w") as f:
            f.write(secret_key)
        print(f"Secret key generated and saved to {SECRET_KEY_FILE}.")
    else:
        print(f"Secret key already exists in {SECRET_KEY_FILE}.")

def get_secret_key() -> str:
    """Read the secret key from the file."""
    if os.path.exists(SECRET_KEY_FILE):
        with open(SECRET_KEY_FILE, "r") as f:
            return f.read().strip()
    else:
        raise FileNotFoundError(
            f"Secret key file '{SECRET_KEY_FILE}' not found. Run generate_secret_key() to create it."
        )
