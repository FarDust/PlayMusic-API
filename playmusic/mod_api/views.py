from playmusic import db
from flask import Blueprint, request, render_template, flash, redirect, url_for
import flask_bootstrap

mod_api = Blueprint('auth',__name__,url_prefix='/api')

@mod_api.route('/<string:post_id>', methods=['GET','POST'])
def index(post_id):
    #db.db.users.find({'_id': post_id})
    return render_template("api/index.html")
