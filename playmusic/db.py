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
            respuesta = { 'mensajes': mensajes }

        except Exception as e:
            print('[ERROR] Ocurrió un error al intentar buscar mensajes', e)
            respuesta = {'error': 'Ocurrió un error en la base de datos.'}

        finally:
            return respuesta


    def mensajes_filtrados(self, obligatorios, quizas, no_pueden):
        """
        Metodo para filtrar mensajes. Recibe una lista con frases obligatorias,
        una lista con palabras que quizás podrían estar y una lista con palabras
        que no pueden estar en los mensajes. 
        Después se escribe una consulta como un string y después se ejecuta
        con eval() y se retorna la lista de mensajes.
        """ 
        try:
            # Base de la query se se ejecutara
            query_aux = "self.db.mensajes.find({\"$text\": {\"$search\": \""
            # Concatenar palabras que quizás pueden ir
            for x in quizas:
                query_aux += "{} ".format(x)
            # Concatenar frases obligatorias que deben estar en el mensaje
            for x in obligatorios:
                query_aux += "\\\"{}\\\" ".format(x)
            # Concatenar palabras que no pueden estar en el mensaje
            for x in no_pueden:
                query_aux += "-{} ".format(x)
            query_aux = query_aux.strip(" ")
            query_aux += "\"}})"
            # Ejecutar la query            
            mensajes =  eval(query_aux)
            mensajes = json.loads(json_util.dumps(mensajes))
            
            print('[DEBUG DB] Mensajes encontrados: ', mensajes)
            respuesta = { 'mensajes': mensajes }

        except Exception as e:
            print('[ERROR] Ocurrió un error al intentar buscar mensajes', e)
            respuesta = { 'error': 'Ocurrió un error en la base de datos.' }

        finally:
            return respuesta