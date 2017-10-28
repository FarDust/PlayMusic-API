import requests
import json


jeison = {
    'obligatorias': ['Tenemos hablar'], 
    'quizas': ['completo'],
    'no_pueden': []
}

jeison = json.dumps(jeison)
print(requests.post('http://localhost:5000/mensajes', json=jeison).text)

