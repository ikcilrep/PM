from app.security.AES import encrypt, decrypt

# Decrypts dictionary encrypted_account and returns Account object with decrypted data.


def decrypt_account(encrypted_account, AES_key):
    # 10: to remove 'encrypted_'
    decrypted = {key[10:]: decrypt(
        encrypted_account[key], AES_key) for key in encrypted_account}
    return Account(decrypted['service_name'], decrypted['username'], decrypted['email'], decrypted['password'])

# Class representing account in some service.


class Account:

    def __init__(self, service_name, username, email, password):
        self.service_name = service_name
        self.username = username
        self.email = email
        self.password = password

    # Encrypts itself and returns dictionary filled with encrypted data.
    # For each information separate IV is used.
    def encrypt(self, AES_key):
        return {
            'encrypted_service_name': encrypt(self.service_name, AES_key),
            'encrypted_username': encrypt(self.username, AES_key),
            'encrypted_email': encrypt(self.email, AES_key),
            'encrypted_password': encrypt(self.password, AES_key)
        }

    def __eq__(self, other):
        return isinstance(other, Account) and self.service_name == other.service_name and self.username == other.username and self.email == other.email and self.password == other.password

    def __neq__(self, other):
        return not self == other
