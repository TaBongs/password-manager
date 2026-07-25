from cryptography.fernet import Fernet

KEY_FILE = ".secret.key"


def load_key():

    with open(KEY_FILE, "rb") as key_file:

        return key_file.read()


key = load_key()

cipher = Fernet(key)


def encrypt_password(password):

    return cipher.encrypt(
        password.encode()
    ).decode()


def decrypt_password(encrypted_password):

    return cipher.decrypt(
        encrypted_password.encode()
    ).decode()