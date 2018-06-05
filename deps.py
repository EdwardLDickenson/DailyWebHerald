from flask import *
from flask_mysqldb import MySQL
from wtforms import *
from wtforms.fields.html5 import EmailField
import crypt
import random
import string
import unicodedata
import json
from datetime import *

import feedparser

app = Flask(__name__)
secrets = open("../secrets.json", "r").read()
results = json.loads(secrets)

app.config["MYSQL_HOST"] = results["MYSQL_HOST"]
app.config["MYSQL_USER"] = results["MYSQL_USER"]
app.config["MYSQL_PASSWORD"] = results["MYSQL_PASSWORD"]
app.config["MYSQL_DB"] = results["MYSQL_DB"]
app.config["MYSQL_CURSORCLASS"] = results["MYSQL_CURSORCLASS"]

mysql = MySQL(app)
app.secret_key = results["secret_key"]
