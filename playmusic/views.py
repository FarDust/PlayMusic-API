from playmusic import app
from flask import render_template
from pymongo import *
import flask_bootstrap


@app.route('/')
def index():
    return render_template("index.html")
