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

@app.route("/")      ################-- dashboard --#######################
def dashboard():

    pass

@app.route("/leaderboard")   ###############-- leaderboard page --#########################
def leaderboard():
    
    pass


##############################################################

if __name__ == "__main__":
    app.run(debug=True)