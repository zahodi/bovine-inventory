# from bovine import staticinventory
from flask import Flask

bovine = Flask(__name__)
from bovine import api
