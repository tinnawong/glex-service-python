from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# app.config.from_pyfile('settings.py')
from demo import views