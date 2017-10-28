from playmusic import app
from flask import render_template, request
from pymongo import *
# import flask_bootstrap


@app.route('/')
def inicio():
    """
    Ruta de inicio de la API. Retorna un simple string
    de bievenida.
    """
    return render_template("index.html")


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
        ret = {'error': 'Ocurrio un error.'}

    finally:
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
        database = db()
        ret = database.buscar_artista_id(int(id))
        status = 200

    except Exception as e:
        status = 500
        ret = {'error': 'Ocurrio un error.'}

    finally:
        respuesta = Response(json.dumps(ret), status=status,
                             mimetype='application/json')
        return respuesta


@app.route('/artista/<id_1>/<id_2>')
def artistas_id(id_1, id_2):
    """
    Tercera ruta del enunciado. Recibe los dos ids de los artistas y
    retorna una lista con todas los mensajes que han intercambiado
    ambos artistas,
    """
    try:
        database = db()
        ret = database.mensajes_compartidos(int(id_1), int(id_2))
        status = 200

    except Exception as e:
        print('[ERROR] Ocurrió un error en mensajes de artistas', e)
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

    Para esta ruta se asume que la base de datos está indexada, si no lo está
    hay que ejecutar: desde mongodb
    db.mensajes.createIndex( { message: 'text' } )
    """
    try:
        # Se recibe lo que se envía al POST y se fuerza a ser JSON
        form = json.loads(request.get_json(force=True))
        database = db()

        print('[DEBUG] Form recibido', form)

        ret = database.mensajes_filtrados(
            form['obligatorias'],
            form['quizas'],
            form['no_pueden'])
        status = 200

    except Exception as e:
        print('[ERROR] Ocurrió un error al buscar mensajes filtrados', e)
        status = 500
        ret = {'error': 'Ocurrió un error.'}

    finally:
        respuesta = Response(json.dumps(ret), status=status,
                             mimetype='application/json')
        return respuesta
