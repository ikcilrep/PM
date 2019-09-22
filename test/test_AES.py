import unittest
import sys
from app.security import AES, secure_generator


class TestAES(unittest.TestCase):
    def test(self):
        for x in range(512):
            key = AES.derive_key(secure_generator.generate_password(x, True, True, True))
            message = secure_generator.generate_password(x, True, True, True) # Random string to be encrypted.
            self.assertEqual(AES.decrypt(AES.encrypt(
                message, key), key), message)
