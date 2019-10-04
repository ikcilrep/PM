from app.security.AES import backend, urandom
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from app.security.base64_str import * 

# Returns new scrypt derivator. 
def get_scrypt_derivator(salt): return Scrypt(
    salt=salt, length=32, n=1048576, r=8, p=1, backend=backend)

# Returns True if password match with stored hash.
def verify_password(password, hash_digest): return to_b64_str(get_scrypt_derivator(
    from_b64_str(hash_digest['salt'])).derive(password.encode())) == hash_digest['hash']

# Returns dictionary with salt ('salt') and result of scrypt derivation for password ('hash'). 
def hash_digest(password):
    salt = urandom(16)
    return {'salt': to_b64_str(salt), 'hash': to_b64_str(get_scrypt_derivator(salt).derive(password.encode()))}
