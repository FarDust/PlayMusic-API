import requests
import json

jeison = json.dumps({ 'opcion': 1, 'data': ['Tenemos que hablar'] })
print(requests.post('http://localhost:5000/mensajes', json=jeison).text)