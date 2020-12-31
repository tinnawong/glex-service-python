from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv('.example_env')

from app import routes