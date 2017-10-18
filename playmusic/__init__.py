from flask import Flask,render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config.from_object('config')

db = PyMongo(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404

from playmusic.mod_api.views import mod_api as api_module

app.register_blueprint(api_module)
#app.register_blueprint(<another module>)
