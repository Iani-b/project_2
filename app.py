from flask import Flask, render_template, jsonify, request, redirect, session
import os
import time
import json
import random
import threading

############################################################

with open("config.json", "r") as config_json:
    config = json.load(config_json)

app = Flask(__name__)
app.secret_key = config["secret_key"]        #idc lol
file_lock = threading.Lock()
invalid_chars = ['{', '}', '[', ']', '/', '\\', '<', '>', '@', ' ', ',']

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

    with file_lock:
        users_json = load_users()

        if not username or any(char in username for char in invalid_chars) or not (2 <= len(username) <= 20):
            return jsonify({"message": "Invalid Username", "type": "invalid_username"})

        if username in users_json:
            return jsonify({"message": "Username already exists", "type": "existing_username"})
        
        if password1 != password2:
            return jsonify({"message": "Passwords do not match", "type": "different_passwords"})
        
        if len(password1) < 6 or not any(char.isdigit() for char in password1) or not any(char.isupper() for char in password1):
            return jsonify({"message": "Password must be at least 6 characters long and contain: A number, An uppercase letter", "type": "invalid_password"})
        
        users_json[username] = {"password": password1}
        save_user(users_json)

    session["username"] = username

    return jsonify({"message": "Signup successful", "type": "signup_success"})

@app.route("/login", methods = ["POST"])
def login():
    
    pass

@app.route("/game")
def game():

    if not logged_in():
        return redirect("/")
 
    return render_template("game.html")

##############################################################

if __name__ == "__main__":
    app.run(debug=True)