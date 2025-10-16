from flask import Flask, render_template, jsonify, request, redirect, session
import os
import time
import json
import random

############################################################

app = Flask(__name__)
app.secret_key = "061338181229718256217153"

##########################################################

def logged_in():
    return 'username' in session


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
            json.dump({}, user_json, indent = 4)
        return {}
    
    
def save_user(users):
    with open("users.json", "w") as user_json:
        json.dump(users, user_json, indent = 4)

##########################################################

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

    session["username"] = username

    return jsonify({"message": "Signup successful"})

@app.route("/login", methods = ["POST"])
def login():
    pass

@app.route("/game")
def game():
    if not logged_in():
        return redirect("/")
 
    return render_template("game.html")

app.run(debug=True)