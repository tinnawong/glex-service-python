
from demo import app

app.config.from_pyfile('settings.py')


@app.route('/')
def index():
    if(app.config.get("API_KEY")):
        return "Hello world : API KEY -> " + str(app.config.get("API_KEY"))
    else:
        return "hello"
