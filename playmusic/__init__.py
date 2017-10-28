from flask import Flask
from flask import Response, send_from_directory, 
                                render_template, request
from flask_pymongo import PyMongo
import json
# Importar modulo de la base de datos
from playmusic.db import Database as db

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def inicio():
    """
    Ruta de inicio de la API. Retorna un simple string
    de bievenida.
    """
    return 'Bienvenido a PlayMusic'


@app.route('/mensajes/<id>')
def mensajes_id(id): 
    """
    Primera rota del enunciado. Recibe el id de un mensaje
    y retorna toda la informacion de este mensaje.
    """
    try: 
        database = db()
        id = int(id)
        ret = database.buscar_mensaje_id(id)
        status = 200

    except Exception as e:
        status = 500
        ret = {'Error': 'Ocurrio un error.'}

    finally:
        respuesta = Response(json.dumps(ret), status = status, mimetype='application/json') 
        return respuesta



# Esto no entendí para que sirve, mejor quizás no complicarse
# con tanto y hacer una api sencilla no más
from playmusic.mod_api.views import mod_api as api_module

app.register_blueprint(api_module)
#app.register_blueprint(<another module>)