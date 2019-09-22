from account import Account
from security.AES import derive_key

class User:
    def __init__(self,accounts, username, AES_key):
        self.accounts = accounts
        self.username = username
        self.AES_key = AES_key
        self.encrypt = lambda: [self.accounts[key].encrypt(self.AES_key) for key in self.accounts]


    def add_account(self, account):
        self.accounts[account.service_name] = account

