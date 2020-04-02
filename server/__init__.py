from flask import Flask

from db import DAL

app = Flask(__name__)
dal = DAL()

from server import routes