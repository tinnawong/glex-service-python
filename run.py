# from dotenv import load_dotenv
from app import app
import os
from gevent.pywsgi import WSGIServer
from flask_cors import CORS

# load_dotenv('.example_env')
CORS(app)
print("Start server :{}:{}".format(os.environ.get("FLASK_RUN_HOST"),os.environ.get("FLASK_RUN_PORT")))
http_server = WSGIServer((str(os.environ.get("FLASK_RUN_HOST")), int(os.environ.get("FLASK_RUN_PORT"))), app)
http_server.serve_forever()