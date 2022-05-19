import binascii
import hashlib
import os


class User:

    def __init__(self, username: str, password: str) -> None:
        self.__username = username
        self.__password = password

    def __str__(self) -> str:
        return f'Admin username: {self.__username}'

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, new_username: str):
        self.__username = new_username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password: str):
        self.__password = new_password

    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdHash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwdHash = binascii.hexlify(pwdHash)
        return (salt + pwdHash).decode('ascii')

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdHash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdHash = binascii.hexlify(pwdHash).decode('ascii')
        return pwdHash == stored_password


# user1 = User("johndoe", "1234")
# user1.username = 'admin'
# user1.password = 'admin'
# password_hash = user1.hash_password(user1.password)
# pass_verify = user1.verify_password(password_hash, user1.username)
#
# if pass_verify:
#     print("Password is same!")
# else:
#     print("Password did not match!")
