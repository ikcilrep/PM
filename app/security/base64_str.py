from base64 import b64encode, b64decode

to_b64_str = lambda x: b64encode(x).decode('ascii') 
from_b64_str = lambda x: b64decode(x.encode('ascii'))

