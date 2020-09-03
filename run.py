from demo import app
from dotenv import load_dotenv
import os
from gevent.pywsgi import WSGIServer
load_dotenv('.env')
print("Start server :127.0.0.1:5200")
http_server = WSGIServer(('127.0.0.1', 5200), app)
http_server.serve_forever()