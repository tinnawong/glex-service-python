import requests
import os
import json
import codecs


class Glex():

    def __init__(self):
        self.typeWord = {0: "UNKNOWN", 1: "KNOWN", 2: "AMBIGUOUS", 3: "ENGLISH",
                         4: "DIGIT", 5: "SPECIAL", 6: "GROUP"}
        self.urlGlexSegment = "http://"+str(os.environ.get("GLEX_HOST"))+":"+str(os.environ.get("GLEX_PORT"))+"/"+"glex/segment"

    def connectGlexService(self,text,fileName,useDict):
        # send text to glex service
        params = dict({"text": text,"useDict":useDict})
        print(self.urlGlexSegment)
        # get respone and create html file
        try:
            response = requests.get(self.urlGlexSegment, params=params)
            if(response.status_code == 200):
                try:
                    response = json.loads(response.text)
                    if(len(response['results']) == len(response['typeLists']) and response['status'] =="ok"):
                        formatToStruct = list(zip(response['results'], response['typeLists']))
                        return {"status": "ok","results":formatToStruct,"fileName":fileName,"dictName":response['dictName']}              
                except Exception as e:
                    return {"status": "failed","message":"can not format json from glex service "}
            else:
                return {"status": "failed","message":"can't connect glex service(status code :{})".format(response.status_code)} 
        except Exception as e:
            return {"status": "failed","message":"can't connect glex service"} 

    def glexSeg(self,text,fileName,useDict):
        return self.connectGlexService(text,fileName,useDict)

    def test(self):
        return {"status": "OK"}


if __name__ == "__main__":
    pass