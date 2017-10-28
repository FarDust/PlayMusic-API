import requests
import json


jeison = {
    'obligatorias': ['Tenemos que hablar'], 
    'quizas': [],
    'no_pueden': ['el']
}

jeison = json.dumps(jeison)
print(requests.post('http://localhost:5000/mensajes', json=jeison).text)

