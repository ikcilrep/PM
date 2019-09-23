from account import Account, decrypt_account
from security.AES import derive_key
from security.password_storing import hash_digest

# Returns decrypted user.


def decrypt_user(encrypted_user, password):
    user = User(
        encrypted_user['username'],
        derive_key(password, encrypted_user['AES_key_salt']),
        password,
        encrypted_user['hashed_password']
    )

    user.assign_accounts(encrypted_user['encrypted_accounts'])
    return user

# Class representing user of this application.


class User:
    def __init__(self, username, AES_key, password, hashed_password):
        self.accounts = {}
        self.username = username
        self.AES_key = AES_key
        self.__hashed_password = hashed_password
        self.__password = password
        self.encrypt = lambda: {
            'username': username,
            'encrypted_accounts': [self.accounts[key].encrypt(self.AES_key) for key in self.accounts],
            'hashed_password': self.__hashed_password,
            'AES_key_salt': self.AES_key['salt']
        }
    def add_account(self, account):
        self.accounts[account.service_name] = account


    # Decrypts and assigns accounts to this user.

    def assign_accounts(self, encrypted_accounts):
        for encrypted_account in encrypted_accounts:
            self.add_account(decrypt_account(encrypted_accounts, self.AES_key))

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password):
        self.__password = new_password
        self.__hashed_password = hash_digest(new_password)
