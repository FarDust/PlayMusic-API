from pymongo import MongoClient
import json
from bson import json_util

# Configuracion para conectarse 
DATABASE = 'test2'
SERVER = 'localhost'
PORT = 27017

class Database:
    """
    Clase principal de la base de datos. Contiene todos los metodos
    de busqueda y los atributos para conectarse a la base de datos en 
    Mongodb.
    """
    def __init__(self):
        try:
            # Cliente de la base de datos
            self.cliente = MongoClient(SERVER, PORT)
            # Base de datos
            self.db = self.cliente[DATABASE]        
        # Malas practicas para manejar errores
        except Exception as e:
            print('[ERROR] Ocurrió un error al intentar conectarse: ', e)


    def buscar_mensaje_id(self, id):
        """
        Metodo para buscar toda la informacion de un mensaje según su
        id. Recibe el id del mensaje, y retorna lo entregado por la base de
        datos.
        """
        try:
            resultado = self.db.mensajes.find({"_id": id})
            resultado = json.loads(json_util.dumps(resultado))
            respuesta = {'informacion': resultado}

        except Exception as e:
            print('[ERROR] Ocurrió un error al buscar informacion del mensaje', e)
            respuesta = {'error': 'Ocurrió un error.'}

        finally:
            return respuesta


    def buscar_artista_id(self, id):
        """
        Metodo para buscar toda la informacion del artista entregado. Además
        entrega una lista con todos los mensajes emitidos por el artista
        """
        try:
            mensajes = self.db.mensajes.find({'sender': id})
            mensajes = json.loads(json_util.dumps(mensajes))
            informacion_usuario = self.db.usuarios.find({'id': id})
            informacion_usuario = json.loads(json_util.dumps(informacion_usuario))
            # Respuesta que se entregará
            respuesta = {'informacion': informacion_usuario, 'mensajes': mensajes}

        except Exception as e:
            print('[ERROR] Ocurrió un un error al intentar buscar info de artista', e)
            respuesta = {'error': 'Ocurrió un error.'}

        finally:
            return respuesta


    def mensajes_compartidos(self, id_1, id_2):
        """
        Metodo para buscar los mensajes que se han enviado entre ellos. Recibe
        los dos id de los usuarios y busca los mensajes emitidos y recibido con
        esos ids y retorna una lista con ellos
        """
        try:
            mensajes = self.db.mensajes.find({'$or': [
                    {"sender": id_1}, 
                    {"receptant": id_1},
                    {"sender": id_2},
                    {"receptant": id_2}
            ]})
            mensajes = json.loads(json_util.dumps(mensajes))
            respuesta = {'mensajes': mensajes}

        except Exception as e:
            print('[ERROR] Ocurrió un error al intentar buscar mensajes', e)
            respuesta = {'error': 'Ocurrió un error en la base de datos.'}

        finally:
            return respuesta