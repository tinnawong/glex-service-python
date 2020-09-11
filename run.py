from dotenv import load_dotenv
from demo import app
import os
from gevent.pywsgi import WSGIServer
from flask_cors import CORS

load_dotenv('.env')
CORS(app)
print("Start server :127.0.0.1:5200")
http_server = WSGIServer(('127.0.0.1', 5200), app)
http_server.serve_forever()