#!/usr/bin/env python3

"""
Hash A Paassword
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
    
    def register_user(self, email: str, password: str) -> User:
        try:
            registeredUser = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(registeredUser.email))
        except NoResultFound:
            self._db.add_user(email, _hash_password(password))


    def valid_login(self, email: str, password: str) -> bool:
        """ Validate Login"""
        try:
            registeredUser = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"), registeredUser.hashed_password) is True:
                return True
            else:
                return False
        except NoResultFound:
            return False
