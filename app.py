from flask import Flask, render_template, jsonify, request, redirect
from datetime import date
import os
import time
import json
import random
import threading

############################################################

app = Flask(__name__)
file_lock = threading.Lock()
invalid_chars = ["{", "}", "[", "]", "/", "\\", "<", ">", "@", " ", ","]

##########################################################


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

@app.route("/") ###
def dashboard():

    return render_template("dashboard.html")

@app.route("/leaderboard") ###
def leaderboard():
    
    return render_template("leaderboard.html")

@app.route("/create_account") ###
def create_account():

    return render_template("create_account.html")

@app.route("/create_account/submit", methods = ["POST"])
def submit_create_account():

    form_submission = request.get_json()
    username = form_submission.get("username")
    password1 = form_submission.get("password1")
    password2 = form_submission.get("password2")
    date_of_birth = form_submission.get("date_of_birth")

    with file_lock:
        users_json = load_users()

        if not username or any(char in username for char in invalid_chars) or not (2 <= len(username) <= 20):
            return jsonify({"message": "Username Must Be 2 To 20 Characters Long And Contain: No Spaces And No Symbols", "type": "warning"})

        if username in users_json:
            return jsonify({"message": "Username Already Exists", "type": "warning"})
        
        if password1 != password2:
            return jsonify({"message": "Passwords Do Not Match", "type": "warning"})
        
        if len(password1) < 6 or not any(char.isdigit() for char in password1) or not any(char.isupper() for char in password1) or " " in password1:
            return jsonify({"message": "Password Must Be At Least 6 Characters Long And Contain: A Number, An Uppercase Letter And No Spaces", "type": "warning"})

        if not date_of_birth or not int(date.today().year) > int(date_of_birth[:4]):
            return jsonify({"message": "Invalid Date Of Birth", "type": "warning"})
       
        users_json[username] = {"password": password1, "date_of_birth": date_of_birth}
        save_user(users_json)

    return jsonify({"message": "Signup successful", "type": "success"})

##############################################################

if __name__ == "__main__":
    app.run(debug=True)