from flask import Flask
from flask import Response, send_from_directory, render_template, request
from flask_pymongo import PyMongo
import json
# Importar modulo de la base de datos
from playmusic.db import Database as db

app = Flask(__name__)
app.config.from_object('config')


@app.errorhandler(404)
def not_found(error):
    respuesta = Response(json.dumps({"error": 404, "description": "route not found"}}), status=status, mimetype='application/json')
    return respuesta

# EMILIO: Esto no entendí para que sirve, mejor quizás no complicarse
# con tanto y hacer una api sencilla no más


# GABRIEL: La idea de esto es para que aprendan a hacer una aplicacion modular
# con flask de tal manera que separen las rutas de manera mas eficiente
# simplemente la siguiente linea llama a la carpeta 'mod_api'.
from playmusic.mod_api.views import mod_api as api_module

app.register_blueprint(api_module)
# app.register_blueprint(<another module>)
