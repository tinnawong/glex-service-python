
from demo import app
from demo.glex.glex import Glex
from flask import request, jsonify
import os
import json
import requests
from demo.WordFrequency.frequency import frequencyWordExpotcsv
glex = Glex()

nlpToolsVersion = os.environ.get("NLPTOOLSVERSION")


app.config['ALLOWED_EXTENSIONS'] = set(['txt'])

# For a given file, return whether it's an allowed type or not


def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def getNameFile(filename):
    name = filename.rsplit(".", 1)
    return str(name[0])


@app.route('/nlptools/ping')
def ping():
    # print("input path >> ",str(os.environ.get("PATH_INPUT")))
    # print("input path >> ",str(os.environ.get("PATH_OUTPUT")))
    return jsonify({"status": "ok", "nlpToolsVersion": nlpToolsVersion})


@app.route('/nlptools/segment', methods=['POST', 'GET'])
def glexSegment():
    print(">>> glex segment")
    #  # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file")
    useDict = request.form['useDict']
    if not uploaded_files or not any(f for f in uploaded_files):
        print("Empty file..")
        return jsonify({"status": "fail", "message": "no file"})
    else:
        filenames = []
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowedFile(file.filename):
                # don't read file befor  ->> print(">>>",str(file.read().decode("utf-8")))
                text = file.read().decode("utf-8")
                print(">>> send to glex service")
                data = glex.glexSeg(text, getNameFile(file.filename), useDict)
                print(">>> send request")

        return jsonify(data)


@app.route('/nlptools/frequency', methods=['POST'])
def frequency():
    filesText = request.files.getlist("files")
    print(filesText)
    print(request.form['fileType'])
    print(request.form["typeOutput"])
    print(request.form['librarySegment'])
    glexDict = ""
    if(request.form['librarySegment'] == "glex"):
        glexDict = request.form['glexDict']
    tupleFile = []
    for f in filesText:
        tupleFile.append((f.filename,f.read().decode("utf-8")))
    free = frequencyWordExpotcsv(TupleFile=tupleFile,
                                 Filetype=request.form['fileType'],
                                 LibraryNumber=request.form['librarySegment'],
                                 selectSystem='fileandfolder',
                                 Dictname=glexDict,
                                 Foldername='corpus 1'
                                 )

    return jsonify({"status": "ok", "results": free.systemfrequencyWordExpotCSV()})

if __name__ == "__main__":
    # from os import environ
    # print(app.config.get('PATH_OUTPUT'))
    pass
