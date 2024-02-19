#!/usr/bin/env python3
"""Flask App"""

from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()

@app.route('/', methods=['GET'])
def jsonpayload() -> str:
    """Json payload delivery"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users() -> str:
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/login', methods=['POST'])
def login() -> str:
    email, passwrd = request.form.get('email'), request.form.get('password')
    if AUTH.valid_login(email, passwrd) is True:
        return jsonify({"message": "your login is Valid"})
    else:
        return jsonify({"message": "your login is invalid"}), 400




if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
