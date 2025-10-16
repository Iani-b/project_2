from flask import Flask, render_template, jsonify, request, redirect
import os
import time
import json
import random

def load_users():
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r") as user_json:
                return json.load(user_json)
        except json.JSONDecodeError:
            print("Error decoding JSON from users.json")
            return {}
    else:
        print("users.json not found")
        with open("users.json", "w") as user_json:
            json.dump({}, user_json)
        return {}
    
def save_user(users):
    with open("users.json", "w") as user_json:
        json.dump(users, user_json)

app = Flask(__name__)

@app.route("/")
def home():
    
    return render_template("home.html")

@app.route("/signup", methods = ["POST"])
def signup():
    
    data = request.get_json()
    username = data.get("username")
    password1 = data.get("password1")
    password2 = data.get("password2")

    users_json = load_users()

    if not username:
        return jsonify({"message": "Username cannot be blank"})

    if username in users_json:
        return jsonify({"message": "Username already exists"})
    
    if password1 != password2:
        return jsonify({"message": "Passwords do not match"})
    
    if len(password1) < 6:
        return jsonify({"message": "Password must be at least 6 characters long"})
    
    users_json[username] = {"password": password1}
    save_user(users_json)
    return jsonify({"message": "Signup successful"})

@app.route("/login")
def login():
    
    pass

@app.route("/game", methods = ["POST"])
def game():
    
    pass

app.run(debug=True)