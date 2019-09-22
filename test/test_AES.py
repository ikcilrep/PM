import unittest
import sys
from security import AES, secure_generator

class Test(unittest.TestCase):
    def test(self):
        for x in range(512):
            password = secure_generator.generate_password(x, False, True, True)
            message = secure_generator.generate_password(x, False, True, True)
            self.assertEqual(AES.decrypt(AES.encrypt(message, password), password), message)
