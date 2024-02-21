#!/usr/bin/env python3
"""Flask App"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """Json payload delivery for home page."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users() -> str:
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST', 'DELETE'])
def login() -> str:
    """
    Create a session for a user
    """
    email, passwrd = request.form.get('email'), request.form.get('password')
    if AUTH.valid_login(email, passwrd) is True:
        if request.method == 'DELETE':
            user = AUTH.get_user_from_session_id(request.cookies['session_id'])
            if user is not None:
                AUTH.destroy_session(user.id)
                return redirect(url_for("/"))
            else:
                return abort(403)
        else:
            session_id = AUTH.create_session(email)
            resp = jsonify({"email": email, "message": "logged in"})
            resp.set_cookie("session_id", session_id)
            return resp
    else:
        return abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
