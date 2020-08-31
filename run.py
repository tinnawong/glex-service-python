from demo import app
from dotenv import load_dotenv
load_dotenv('.env')
# app.run(port=5200)
# from gevent.pywsgi import WSGIServer
# print("Start ")
# http_server = WSGIServer(('', 5200), app)
# http_server.serve_forever()