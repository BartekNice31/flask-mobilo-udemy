import string
import hashlib
import binascii
import datetime
import random
import os

class User:
    def __init__(self,user='',password=''):
        self.user=user
        self.password=password
    def hash_password(self):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
class UserPass:
    def __init__(self,user='',password=''):
        self.user=user
        self.password=password
    def hash_password(self):
        """Hash a password for storing."""
        # the value generated using os.urandom(60)
        os_urandom_static = b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xaa\x05\xccc\xc2\xe8K\xcf\xf1\xac\x9bFy(\xfbn.`\xe9\xcd\xdd'\xdf`~vm\xae\xf2\x93WD\x04"
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii') 
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000) 
        pwdhash = binascii.hexlify(pwdhash) 
        return (salt + pwdhash).decode('ascii')
    def verify_password(self, stored_password, provided_password):
        """    Verify a stored password against one provided by user.    """
        salt = stored_password[:64]
        stored_password = stored_password[64:]

        pwdhash = hashlib.pbkdf2_hmac('sha512',
            provided_password.encode('utf-8'),
            salt.encode('ascii'),
            100000
        )

        pwdhash = binascii.hexlify(pwdhash).decode('ascii')

        return pwdhash == stored_password


    def get_random_user_password(self):
        random_user = ''.join(
            random.choice(string.ascii_lowercase)
            for i in range(3)
        )

        self.user = random_user

        password_characters = string.ascii_letters
        # password_characters = (
        #     string.ascii_letters +
        #     string.digits +
        #     string.punctuation
        # )

        random_password = ''.join(
            random.choice(password_characters)
            for i in range(3)
        )

        self.password = random_password