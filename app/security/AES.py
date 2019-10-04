from app.security.base64_str import * 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from os import urandom

backend = default_backend()
pkcs7 = padding.PKCS7(128)

# Returns pbkdf2 derivators: one for key, one for IV.
def derive_key(password, salt=to_b64_str(urandom(16))):
    return {
            'key': to_b64_str(PBKDF2HMAC(algorithm=SHA256, length=32, salt=from_b64_str(salt), iterations=100000, backend=backend).derive(password.encode('utf-8'))),
            'salt': salt
            }


# Returns dictionary with ciphertext ('ciphertext') and initialization vector ('IV').

def encrypt(data, key):
    padder = pkcs7.padder()
    IV = urandom(16)
    encryptor = Cipher(algorithms.AES(from_b64_str(key['key'])), modes.CBC(IV),
                       backend=backend).encryptor()
    return {'ciphertext': to_b64_str(encryptor.update(padder.update(data.encode('utf-8')) + padder.finalize()) + encryptor.finalize()), 'IV': to_b64_str(IV)}

# Returns returns decrypted data.


def decrypt(encrypted_data, key):
    unpadder = pkcs7.unpadder()
    decryptor = Cipher(algorithms.AES(from_b64_str(key['key'])), modes.CBC(from_b64_str(
        encrypted_data['IV'])), backend=backend).decryptor()
    return (unpadder.update(decryptor.update(from_b64_str(encrypted_data['ciphertext'])) + decryptor.finalize()) + unpadder.finalize()).decode('utf-8')
