import os, json
from flask import Flask
from flask_feather import Feather
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from os import path


if path.exists(".env"):
    load_dotenv()

app = Flask(__name__)
app.secret_key = 'Th!$I$Th3K3y4Th3I@C@ppl!c@t!0n'
feather = Feather(app)

stats={"current":{},"next":{}}

from app import routes

