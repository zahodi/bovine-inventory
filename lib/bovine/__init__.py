# from bovine import staticinventory
from flask import Flask

api = Flask(__name__)
from bovine import views
