import re
import pyotp
from passlib.hash import pbkdf2_sha512

class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w\-\.]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def generate_auth_code():
        # returns a 16 character base32 secret. Compatible with Google Authenticator and other OTP apps
        return pyotp.random_base32()

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        return pbkdf2_sha512.verify(password, hashed_password)
