import sys
from os import listdir, sep
from pymongo import MongoClient
import json

DATABASE = 'test2'
SERVER = 'localhost'
PORT = 27017

cliente = MongoClient(SERVER, PORT)
db = cliente[DATABASE]


def id_generator():
    i = 0
    yield
    while True:
        yield i
        i += 1


ids = id_generator()

if len(sys.argv) == 2:
    if sys.argv[1] in listdir("./"):
        with open(sys.argv[1], "rb") as file:
            data = json.loads(file.read())
        # Guarda los json en la coleccion con el nombre de archivo
        collection = sys.argv[1].split(".")[0]
        for obj in data:
            if not "id" in obj.keys():
                obj["_id"] = next(ids)
            if "id" in obj:
                obj["_id"] = obj["id"]
                obj.pop("id", 0)
            db[collection].insert_one(obj)
            print("item id: {} ready!!!".format(obj["id"]))
    else:
        raise FileNotFoundError
else:
    raise AttributeError
