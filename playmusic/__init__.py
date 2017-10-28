from flask import Flask
from flask import Response, send_from_directory, render_template, request
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
        ret = {'error': 'Ocurrio un error.'}

    finally:
        respuesta = Response(json.dumps(ret), status = status, mimetype='application/json') 
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
        respuesta = Response(json.dumps(ret), status=status, mimetype='application/json')
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
        respuesta = Response(json.dumps(ret), status=status, mimetype='application/json')
        return respuesta


@app.route('/mensajes', methods=['POST'])
def mensajes_filtrados():
    """
    Cuarta ruta con tres opciones, solamente acepta POST. Recibe un 
    json con la opcion y los datos a filtrar
    """
    try: 
        # Se recibe lo que se envía al POST y se fuerza a ser JSON
        form = json.loads(request.get_json(force=True))
        database = db()

        print('[DEBUG] Form recibido', form)

        if form['opcion']:
            # Agregar una o más frases si o si deben estar en el mensaje
            if form['opcion'] == 1:
                if len(form['data']) > 0:
                    # Concatenar frases en una sola frase gigante
                    ret = database.mensajes_filtrados_frases(form['data'])
                else:
                    ret = {'error': 'La lista de frases está vacía'}

            # Agregar palabras que deseablemente deben estar pero no necesarias
            elif form['opcion'] == 2:
                if len(form['data']) > 0:
                    # Concatenar palabras en una sola frase
                    palabras = ''
                    for x in form['data']:
                        frases += ' {}'.format(x)


            # Agregar palabras que no pueden estar en el mensaje
            elif form['opcion'] == 3:
                pass

            status = 200
        
        else: 
            print('[ERROR] Ocurrió un error no se encontró la opción')
            ret = {'error': 'No se encontró opcion'}

    except Exception as e:
        print('[ERROR] Ocurrió un error al buscar mensajes filtrados', e)
        status = 500
        ret = {'error': 'Ocurrió un error.'}

    finally:
        respuesta = Response(json.dumps(ret), status=status, mimetype='application/json')
        return respuesta



# Esto no entendí para que sirve, mejor quizás no complicarse
# con tanto y hacer una api sencilla no más
from playmusic.mod_api.views import mod_api as api_module

app.register_blueprint(api_module)
#app.register_blueprint(<another module>)