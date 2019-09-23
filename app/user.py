from account import Account, decrypt_account
from security.AES import derive_key
from security.password_storing import hash_digest


class User:
    def __init__(self, username, AES_key, password, hashed_password):
        self.username = username
        self.AES_key = AES_key
        self.__hashed_password = hashed_password
        self.__password = password
        self.encrypt = lambda: [self.accounts[key].encrypt(
            self.AES_key) for key in self.accounts]

    def assign_accounts(self, encrypted_accounts, AES_key):
        def add_account(self, account):
            self.accounts[account.service_name] = account

        self.accounts = {}
        for encrypted_account in encrypted_accounts:
            self.add_account(decrypt_account(encrypted_accounts, AES_key))

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password):
        self.__password = new_password
        self.__hashed_password = hash_digest(new_password)
