import unittest
import sys
from app.security.AES import derive_key
from app.account import Account, decrypt_account


class TestAccount(unittest.TestCase):
    def test(self):
        account = Account("service", "username", "email", "password")
        key = derive_key("user_password")
        self.assertEquals(account, decrypt_account(account.encrypt(key), key))
