from flask import Flask, render_template, jsonify, request, redirect
import os
import time
import json
import random
import threading

############################################################

with open("config.json", "r") as config_json:
    config = json.load(config_json)

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

@app.route("/")      ################-- dashboard --#######################
def dashboard():

    return render_template("dashboard.html")

@app.route("/leaderboard")   ###############-- leaderboard page --#########################
def leaderboard():
    
    return render_template("leaderboard.html")


##############################################################

if __name__ == "__main__":
    app.run(debug=True)