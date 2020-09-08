from demo import app
import os
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
CORS(app)
# print("Start serve : ",os.environ.get("FLASK_RUN_HOST"),":", int(os.environ.get("FLASK_RUN_PORT")))
# http_server = WSGIServer((os.environ.get("FLASK_RUN_HOST"), int(os.environ.get("FLASK_RUN_PORT"))), app)
print("Start server : 127.0.0.1:5200")
http_server = WSGIServer(("127.0.0.1", 5200), app)
http_server.serve_forever()