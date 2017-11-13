from playmusic import app
from flask import render_template, request, Response, send_from_directory, request
from pymongo import *
from playmusic.db import Database as DB
import json
# import flask_bootstrap


@app.route('/')
def inicio():
    """
    Ruta de inicio de la API. Retorna un simple string
    de bievenida.
    """
    return render_template("index.html")


@app.route('/mensajes', methods=['GET'])
def mensajes_id():
    """
    Primera ruta del enunciado. Recibe el id de un mensaje
    y retorna toda la informacion de este mensaje.
    """
    id = request.args.get("id")
    database = DB()
    id = int(id)
    ret = database.buscar_mensaje_id(id)
    
    status = 200
    respuesta = Response(json.dumps(ret), status=status,
                         mimetype='application/json') 
    return respuesta


@app.route('/artista/<id>')
def artista_id(id):
    """
    Segunda ruta del enunciado. Recibe el id del artista y retorna
    toda la informacion del usuario y una lista con todos los
    mensajes enviados por el usuario
    """
    try:
        database = DB()
        ret = database.buscar_artista_id(int(id))
        status = 200

    except Exception as e:
        status = 500
        ret = {'error': 'Ocurrio un error.'}

    finally:
        respuesta = Response(json.dumps(ret), status=status,
                             mimetype='application/json')
        return respuesta


@app.route('/artista')
def artistas_id():
    """
    Tercera ruta del enunciado. Recibe los dos ids de los artistas y
    retorna una lista con todas los mensajes que han intercambiado
    ambos artistas,
    """
    id_1 = request.args.get("id1")
    id_2 = request.args.get("id2")
    try:
        database = DB()
        ret = database.mensajes_compartidos(int(id_1), int(id_2))
        status = 200

    except Exception as e:
        print('[ERROR] Ocurrio un error en mensajes de artistas', e)
        status = 500
        ret = {'error': 'Ocurrio un error.'}

    finally:
        respuesta = Response(json.dumps(ret), status=status,
                             mimetype='application/json')
        return respuesta


@app.route('/mensajes', methods=['POST'])
def mensajes_filtrados():
    """
    Cuarta ruta con tres opciones, solamente acepta POST. Recibe un
    json con la opcion y los datos a filtrar.

    Para esta ruta se asume que la base de datos esta indexada, si no lo esta
    hay que ejecutar desde mongodb
    db.mensajes.createIndex( { message: 'text' } )
    """
    try:
        # Se recibe lo que se envia al POST y se fuerza a ser JSON
        form = request.get_json()
        database = DB()


        print('[DEBUG] Form recibido', form)

        ret = database.mensajes_filtrados(
            form['obligatorias'],
            form['quizas'],
            form['no_pueden'])
        status = 200

    except Exception as e:
        print('[ERROR] Ocurrió un error al buscar mensajes filtrados', e)
        status = 500
        ret = {'error': 'Ocurrio un error.'}

    finally:
        respuesta = Response(json.dumps(ret), status=status,
                             mimetype='application/json')
        return respuesta
