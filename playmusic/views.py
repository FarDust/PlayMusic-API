from playmusic import app
from flask import render_template, request
from pymongo import *
# import flask_bootstrap


@app.route('/')
def index():
    bar = request.args.to_dict()
    if "a" in bar and "b" in bar:
        return str(bar["a"]) + " " + str(bar["b"]), 200
    else:
        return render_template("404.html"), 404
