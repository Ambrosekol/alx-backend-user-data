#!/usr/bin/env python3

"""
Hash A Paassword
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Optional


def _hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def _generate_uuid() -> str:
        uuid = uuid4()
        return str(uuid)


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


    def create_session(self, email: str) -> Optional[str | None]:
        user = None
        try:
            user = self._db.find_user_by(email=email)
            generateSessionId = _generate_uuid()
            user.session_id = generateSessionId
            return generateSessionId
        except NoResultFound:
            return user
