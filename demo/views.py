
from demo import app

app.config.from_pyfile('settings.py')


@app.route('/')
def index():
    return "Hello world : API KEY -> " + str(app.config.get("API_KEY"))
