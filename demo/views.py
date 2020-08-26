
from demo import app
from demo.glex.glex import Glex
from flask import request,jsonify
import os ,json
from flask_cors import CORS

app.config.from_pyfile('settings.py')
glex = Glex()
CORS(app)

@app.route('/',methods =['POST','GET'])
def index():
    # data = glexSeg("glexSeg")
    
    data = " -> method > "
    if request.method == 'POST':
        data = data + "POST"
    elif request.method == 'GET':
        data = data + "GET"
    else :
        data = data + "not allow"
    return data

@app.route('/test',methods =['POST','GET'])
def testPaht():
    print("input path >> ",str(os.environ.get("PATH_INPUT")))
    print("input path >> ",str(os.environ.get("PATH_OUTPUT")))
    return "success"


app.config['ALLOWED_EXTENSIONS'] = set(['txt'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def getNameFile(filename):
    name = filename.rsplit(".", 1)
    return str(name[0])

@app.route('/glexSegment',methods =['POST','GET'])
def glexControl():
    print(">>> glex segment")
    #  # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file")
    if not uploaded_files or not any(f for f in uploaded_files):
        print("Empty file..")
        return jsonify({"status": "fail","message":"no file"})
    else:
        filenames = []
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):                
                # don't read file befor  ->> print(">>>",str(file.read().decode("utf-8")))
                text = file.read().decode("utf-8")
                print(">>> text send :",text)
                data = glex.glexSeg(text,getNameFile(file.filename))
                print(data)
    
        return jsonify(data)

if __name__ == "__main__":
    # from os import environ 
    # print(app.config.get('PATH_OUTPUT'))
    pass