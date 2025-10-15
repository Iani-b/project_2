from flask import Flask, render_template, jsonify, request, redirect
import os
import time
import json
import random

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods = "POST")
def signup():
    pass

@app.route("/login")
def login():
    pass

@app.route("/game", methods = "POST")
def game():
    pass