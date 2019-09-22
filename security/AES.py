from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from os import urandom

backend = default_backend()
pkcs7 = padding.PKCS7(128)

# Returns pbkdf2 derivators: one for key, one for IV.


def get_derivators(saltKey, saltIV):
    pbkdf2Key = PBKDF2HMAC(algorithm=SHA256, length=32,
                           salt=saltKey, iterations=100000, backend=backend)
    pbkdf2IV = PBKDF2HMAC(algorithm=SHA256, length=16,
                          salt=saltIV, iterations=100000, backend=backend)
    return pbkdf2Key, pbkdf2IV

# Returns tuple (saltKey, saltIV, encrypted_data), where encrypted_data is data encrypted with AES and salts are random bytes.


def encrypt(data, password):
    padder = pkcs7.padder()
    saltKey, saltIV = urandom(16), urandom(16)
    pbkdf2Key, pbkdf2IV = get_derivators(saltKey, saltIV)
    password = password.encode('utf-8')
    key = pbkdf2Key.derive(password)
    IV = pbkdf2IV.derive(password)
    cipher = Cipher(algorithms.AES(key), modes.CBC(IV), backend=backend)
    encryptor = cipher.encryptor()
    return (saltKey, saltIV, encryptor.update(padder.update(data.encode('utf-8')) + padder.finalize()) + encryptor.finalize())

# Returns returns decrypted data.


def decrypt(encrypted_data, password):
    unpadder = pkcs7.unpadder()
    saltKey, saltIV = encrypted_data[0], encrypted_data[1]
    pbkdf2Key, pbkdf2IV = get_derivators(saltKey, saltIV)
    password = password.encode('utf-8')
    key = pbkdf2Key.derive(password)
    IV = pbkdf2IV.derive(password)
    cipher = Cipher(algorithms.AES(key), modes.CBC(IV), backend=backend)
    decryptor = cipher.decryptor()
    return (unpadder.update(decryptor.update(encrypted_data[2]) + decryptor.finalize()) + unpadder.finalize()).decode('utf-8')
