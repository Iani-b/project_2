from flask import Flask, render_template, jsonify, request, redirect
import os
import time
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")