
from app import app
from app.glex.glex import Glex
from flask import request, jsonify
import flask
import os
import json
import requests
from app.WordFrequency.frequency import FrequencyWord

glex = Glex()

nlpToolsVersion = os.environ.get("NLPTOOLSVERSION")
app.config['ALLOWED_EXTENSIONS'] = set(['txt'])

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def getNameFile(filename):
    name = filename.rsplit(".", 1)
    return str(name[0])

@app.route('/nlptools/ping')
def ping():
    return jsonify({"status": "ok", "nlpToolsVersion": nlpToolsVersion})

@app.route('/nlptools/segment', methods=['POST', 'GET'])
def glexSegment():
    #  # Get the name of the uploaded files
    fileUpload = request.files.getlist("file")
    useDict = request.form['useDict']
    if not fileUpload or not any(f for f in fileUpload):
        return jsonify({"status": "fail", "message": "file empty"})
    else:
        filenames = []
        for file in fileUpload:
            # Check if the file is one of the allowed types/extensions
            if file and allowedFile(file.filename):
                text = file.read().decode("utf-8")
                data = glex.glexSeg(text, getNameFile(file.filename), useDict)

        return jsonify({"status": "ok", "result": data})

@app.route('/nlptools/frequency', methods=['POST'])
def frequency():
    filesText = request.files.getlist("files")
    if(len(filesText)==0):
        flask.abort(400)
        return
    if(not request.form['fileType'] or not request.form['librarySegment'] or not request.form["typeOutput"]):
        flask.abort(400)
        return
    glexDict = ""
    if(request.form['librarySegment'] == "glex"):
        glexDict = request.form['glexDict']
    tupleFile = []
    for f in filesText:
        tupleFile.append((f.filename,f.read().decode("utf-8")))
    frequency = FrequencyWord(TupleFile=tupleFile,
                                 Filetype=request.form['fileType'],
                                 LibraryNumber=request.form['librarySegment'],
                                 selectSystem=request.form["typeOutput"],
                                 Dictname=glexDict,
                                 Foldername=request.form["corpusName"],
                                 )
    result = frequency.systemfrequencyWordExpotCSV()
    if result ==[]:
        return jsonify({"status": "fail", "message": "no output file"})
    else:
        return jsonify({"status": "ok", "results":result })

if __name__ == "__main__":
    pass
