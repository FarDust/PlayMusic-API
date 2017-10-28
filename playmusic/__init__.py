from flask import Flask
from flask import Response, send_from_directory, render_template, request
from flask_pymongo import PyMongo
import json
# Importar modulo de la base de datos
from playmusic.db import Database as db

app = Flask(__name__)
app.config.from_object('config')

# EMILIO: Esto no entendí para que sirve, mejor quizás no complicarse
# con tanto y hacer una api sencilla no más

# GABRIEL: La idea de esto es para que aprendan a hacer una aplicacion modular
# con flask de tal manera que separen las rutas de manera mas eficiente
# simplemente la siguiente linea llama a la carpeta 'mod_api'.
from playmusic.mod_api.views import mod_api as api_module

app.register_blueprint(api_module)
# app.register_blueprint(<another module>)
