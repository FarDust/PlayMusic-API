import sys
from os import listdir, sep
from pymongo import MongoClient
import json

DATABASE = 'test2'
SERVER = 'localhost'
PORT = 27017

cliente = MongoClient(SERVER, PORT)
db = self.cliente[DATABASE]

if len(sys.argv) == 2:
    if sys.argv[1] in listdir("./"):
        with open(sys.argv[1], "rb") as file:
            data = json.loads(file.read())
        # Guarda los json en la coleccion con el nombre de archivo
        collection = sys.argv[1].split(".")[0]
        for obj in data:
            db[collection].insert_one(obj)
    else:
        raise FileNotFoundError
else:
    raise AttributeError
