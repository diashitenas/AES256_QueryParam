from cryptography.hazmat.primitives import keywrap
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

key = os.urandom(32)  

with open("secret.key", "wb") as key_file:
    key_file.write(key)