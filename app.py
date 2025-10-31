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


def load_file(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, "r") as file_json:
                return json.load(file_json)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_name}")
            return {}
    else:
        print(f"{file_name} not found")
        with open(file_name, "w") as file_json:
            json.dump({}, file_json, indent = 4)
        return {}
    
    
def save_file(file_name, data):
    with open(file_name, "w") as file_json:
        json.dump(data, file_json, indent = 4)


##########################################################

@app.route("/") #-- Dashboard --#
def dashboard():

    return render_template("dashboard.html")

@app.route("/leaderboard") #-- Leaderboards --#
def leaderboard():

    with file_lock:
        leaderboard_json = load_file("leaderboard.json")

    leaderboard = sorted(leaderboard_json, key=lambda score_size: score_size["score"], reverse=True)

    return render_template("leaderboard.html", leaderboard=leaderboard)

@app.route("/create_account") #-- Creating Account --#
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
        users_json = load_file("users.json")

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
        save_file("users.json", users_json)
    
    return jsonify({"message": "Signup successful", "type": "success"})

@app.route("/view_accounts") #-- View player details --#
def view_accounts():

    return render_template("view_accounts.html")

@app.route("/view_accounts/find", methods = ["POST"])
def view_accounts_find():

    username_submission = request.get_json()
    needed_username = username_submission.get("username")

    with file_lock:
        users_json = load_file("users.json")

        if needed_username in users_json:
            user_data = users_json.get(needed_username)
            return jsonify({"date_of_birth": f"Date Of Birth: {user_data.get("date_of_birth", "N/A")}",
                            "last_game": f"Last Game's Result: {user_data.get("last_game", "N/A")}",
                            "wins": f"Wins: {user_data.get("wins", "N/A")}",
                            "losses": f"Losses: {user_data.get("losses", "N/A")}",
                            "type": "success"})
        
    return jsonify({"message": "The Desired User Does Not Exist", "type": "warning"})

@app.route("/game")
def game():

    return render_template("game.html")

@app.route("/game/round", methods = ["POST"])
def game_round():

    pass

##############################################################

if __name__ == "__main__":
    app.run(debug=True)