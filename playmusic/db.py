from pymongo import MongoClient
import json
from bson import json_util

# Configuracion para conectarse 
DATABASE = 'test'
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
            resultado = self.db.mensajes.find({"mid": id})
            respuesta = json.loads(json_util.dumps(resultado))

        except Exception as e:
            print('[ERROR] Ocurrió un error al buscar informacion del mensaje', e)
            respuesta = False

        finally:
            return respuesta