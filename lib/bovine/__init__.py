# from bovine import staticinventory
from flask import Flask

app = Flask(__name__)
from bovine import views
