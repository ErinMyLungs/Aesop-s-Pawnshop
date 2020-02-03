# Dashboard entry file
from flask import Flask
import pandas as pd
import numpy as np
from pymongo_db import db

# TODO: Refactor this to hell and back because it's currently pretty terrible

collection = db["frontend"]

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

if __name__ == '__main__':
    app.run(debug=True)
