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
invalid_chars = ["{", "}", "[", "]", "/", "\\", "<", ">", "@", " ", ","]

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

@app.route("/")      ################-- login and signup page --#######################
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
            return jsonify({"message": "Username Must Be 2 To 20 Characters Long And Contain: No Spaces And No Symbols", "type": "invalid_username"})

        if username in users_json:
            return jsonify({"message": "Username Already Exists", "type": "existing_username"})
        
        if password1 != password2:
            return jsonify({"message": "Passwords Do Not Match", "type": "different_passwords"})
        
        if len(password1) < 6 or not any(char.isdigit() for char in password1) or not any(char.isupper() for char in password1):
            return jsonify({"message": "Password Must Be At Least 6 Characters Long And Contain: A Number and An Uppercase Letter", "type": "invalid_password"})
        
        users_json[username] = {"password": password1}
        save_user(users_json)

    session["username"] = username

    return jsonify({"message": "Signup successful", "type": "signup_success"})

@app.route("/login", methods = ["POST"])
def login():
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    with file_lock:
        users_json = load_users()

        if username not in users_json:
            return jsonify({"message": "Username Does Not Exist", "type": "invalid_username"})
        
        if password != users_json[username]["password"]:
            return jsonify({"message": "Incorrect Password", "type": "invalid_password"})
        
    session["username"] = username

    return jsonify({"message": "Login successful", "type": "login_success"})
        
@app.route("/dashboard")   ##################-- dashboard page --##########################
def dashboard():

    if not logged_in():
        return redirect("/")
 
    return render_template("dashboard.html")

@app.route("/dashboard/logout", methods = ["POST"])
def dashboard_logout():

    data = request.get_json()
    log_out = data.get("log_out")

    if log_out:
        session.clear()
        return jsonify({"message": "You Have Logged Out", "type": "success"})
    
    return jsonify({"message": "Something Went Wrong", "type": "error"})

@app.route("/leaderboard")   ###############-- leaderboard page --#########################
def leaderboard():
    
    pass


##############################################################

if __name__ == "__main__":
    app.run(debug=True)