#!/usr/bin/env python3
"""This Module Contains code for the actual endpoints callable"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def index() -> str:
    """GET /
     Return:
    - The home page's payload.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    Create a new user in the db
    """
    email, password = request.form.get("email"), request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Create a session for a user
    """
    email, passwrd = request.form.get('email'), request.form.get('password')
    if AUTH.valid_login(email, passwrd) is True:
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    This logs the user out of the session
    """
    sessionId = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(sessionId)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """
    Returns the user profile (email)
    """
    sessionId = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(sessionId)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def reset_password() -> str:
    """
    Send a reset token for password
    """
    email = request.cookies.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def resetPassword() -> str:
    """
    Reset password to a new password
    """
    email = request.form.get("email")
    token = request.form.get("reset_token")
    Passwrd = request.form.get("new_password")
    try:
        AUTH.update_password(token, Passwrd)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
