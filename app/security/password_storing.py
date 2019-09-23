from app.security.AES import backend, urandom
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

# Returns new scrypt derivator. 
def get_scrypt_derivator(salt): return Scrypt(
    salt=salt, length=32, n=1048576, r=8, p=1, backend=backend)

# Returns True if password match with stored hash.
def verify_password(password, hash_digest): return get_scrypt_derivator(
    stored_hashed_password['salt']).derive(password.encode('utf-8')) == stored_hashed_password['hash']

# Returns dictionary with salt ('salt') and result of scrypt derivation for password ('hash'). 
def hash_digest(password):
    salt = urandom(16)
    return {'salt': salt, 'hash': get_scrypt_derivator(salt).derive(password.encode('utf-8'))}
