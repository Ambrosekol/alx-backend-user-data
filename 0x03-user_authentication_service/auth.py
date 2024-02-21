#!/usr/bin/env python3

"""
Hash A Paassword
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Optional, Union


def _hash_password(password: str) -> bytes:
    """
    This hashes the string password into bytes
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generate unique UUID string"""
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
        except NoResultFound:
            new_user = self._db.add_user(email, _hash_password(password))
            return new_user
        else:
            raise ValueError("User {} already exists"
                             .format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ Validate Login"""
        try:
            registeredUser = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode("utf-8"),
                              registeredUser.hashed_password) is True:
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Optional[str | None]:
        """
        Create a session for the user
        and return a session UUID
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            generateSessionId = _generate_uuid()
            self._db.update_user(user.id, session_id=generateSessionId)
            return generateSessionId
        except NoResultFound:
            return user

    def get_user_from_session_id(self, session_id: Union[str | None]
                                 ) -> Union[User | None]:
        """Gets user from a given session ID string"""
        if session_id is not None:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy a user ID Session"""
        self._db.update_user(user_id, session_id=None)
