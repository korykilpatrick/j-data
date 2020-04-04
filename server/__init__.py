from flask import Flask
from flask_cors import CORS

# from db import DAL

app = Flask(__name__)
CORS(app)

# dal = DAL()

from server.routes import game, user, auth