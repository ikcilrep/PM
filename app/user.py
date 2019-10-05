from app.account import Account, decrypt_account
from app.security.AES import derive_key
from app.security.password_storing import hash_digest
from app.security.base64_str import *
from os import path
import json
from base64 import urlsafe_b64encode

# Returns unique path for every username.
def get_path_by_username(username):
    return path.join('data', 'data_' + urlsafe_b64encode(username.encode()).decode('ascii') + '.json')


# Reads and returns encrypted user from file.
def read_encrypted_user(username):
    with open(get_path_by_username(username), 'r') as f:
        return json.load(f)

# Returns true if user with given username exists.
def does_user_exist(username):
    return path.exists(get_path_by_username(username))


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
        self.accounts = [] 
        self.username = username
        self.AES_key = AES_key
        self.__hashed_password = hashed_password
        self.__password = password
       
    def encrypt(self): 
        return {
            'username': self.username,
            'encrypted_accounts': [account.encrypt(self.AES_key) for account in self.accounts],
            'hashed_password': self.__hashed_password,
            'AES_key_salt': self.AES_key['salt']
        }

    def add_account(self, account):
        self.accounts.append(account)


    # Decrypts and assigns accounts to this user.

    def assign_accounts(self, encrypted_accounts):
        for encrypted_account in encrypted_accounts:
            self.add_account(decrypt_account(encrypted_account, self.AES_key))


    def save(self):
        encrypted = self.encrypt()
        
        with open(get_path_by_username(self.username), 'w') as f:
          f.write(json.dumps(self.encrypt()))

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password):
        self.__password = new_password
        self.__hashed_password = hash_digest(new_password)
        self.AES_key = derive_key(self.__password)
