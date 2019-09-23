import unittest
import sys
from app.security.AES import derive_key
from app.security.password_storing import hash_digest
from app.account import Account, decrypt_account
from app.user import *

class TestAccount(unittest.TestCase):
    def test(self):
        password = "user_password"
        key = derive_key(password)
        user = User("username1", key,  password, hash_digest(password)) 
        user.add_account(Account("service", "username", "email", "password"))

        dictionary_user = vars(user)
        dictionary_decrypted_user = vars(decrypt_user(user.encrypt(), password))

        for key in dictionary_user:
            self.assertEqual(dictionary_user[key], dictionary_decrypted_user[key])
