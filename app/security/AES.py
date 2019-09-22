from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from os import urandom

backend = default_backend()
pkcs7 = padding.PKCS7(128)

# Returns pbkdf2 derivators: one for key, one for IV.


def derive_key(password, salt=urandom(16)):
    return {'key': PBKDF2HMAC(algorithm=SHA256, length=32, salt=salt, iterations=100000, backend=backend).derive(password.encode('utf-8')), 'salt': salt}


# Returns dictionary with ciphertext ('ciphertext') and initialization vector ('IV').

def encrypt(data, key):
    padder = pkcs7.padder()
    IV = urandom(16)
    encryptor = Cipher(algorithms.AES(key['key']), modes.CBC(IV),
                       backend=backend).encryptor()
    return {'ciphertext': encryptor.update(padder.update(data.encode('utf-8')) + padder.finalize()) + encryptor.finalize(), 'IV': IV}

# Returns returns decrypted data.


def decrypt(encrypted_data, key):
    unpadder = pkcs7.unpadder()
    decryptor = Cipher(algorithms.AES(key['key']), modes.CBC(
        encrypted_data['IV']), backend=backend).decryptor()
    return (unpadder.update(decryptor.update(encrypted_data['ciphertext']) + decryptor.finalize()) + unpadder.finalize()).decode('utf-8')
