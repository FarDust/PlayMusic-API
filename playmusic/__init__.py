from flask import Flask
from requests import get,post,put

app = Flask(__name__)

import users.views

if __name__ == "__main__":
    app.run()
