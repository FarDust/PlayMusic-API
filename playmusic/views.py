from users import app
from flask import render_template
import flask_bootstrap


@app.route('/')
def index():
    return render_template("index")
