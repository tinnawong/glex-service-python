
import requests
import os
import json
import codecs


class Glex():

    def __init__(self):
        self.typeWord = {0: "UNKNOWN", 1: "KNOWN", 2: "AMBIGUOUS", 3: "ENGLISH",
                         4: "DIGIT", 5: "SPECIAL", 6: "GROUP"}
        self.hostingGlex = str(os.environ.get("HOSTING_GLEX_SEGMENT"))

    # def readFile(self.path):
    #     pass
    #     # with open(self.path, 'r', encoding="utf-8") as file:
    #     #     file = file.read()
    #     # return file
    def creatHTML(self, results, typeLists,fileName):
        print(">>> creat html")
        html = """<!DOCTYPE html><html><head>
        <title></title>
        <style>
            body {
                margin: 20px;
            }
            
            .UNKNOWN {
                background-color: #FF1100;
            }
            
            .KNOWN {
                background-color: #00AB36;
            }
            
            .AMBIGUOUS {
                background-color: #0800FF;
            }
            
            .ENGLISH {
                background-color: #99989C;
            }

            .DIGIT {
                background-color: #EBB326;
            }
            .SPECIAL {
                background-color: #ffa50099;
            }

            .GROUP {
                background-color: #964B00;
            }
            
            .box {
                /* border: 1px solid #000; */
                width: 2em;
                padding-left: 1em;
            
            }
        </style>
        </head><body>
        """
        html += """
        <div class="row" style="text-align: center;">            
            <span class="box UNKNOWN"></span><span>คำที่ไม่รู้จัก</span>&nbsp;|&nbsp;
            <span class="box KNOWN"></span><span>คำที่รู้จัก</span>&nbsp;|&nbsp;
            <span class="box AMBIGUOUS"></span><span>คำกำกวม</span>&nbsp;|&nbsp;
            <span class="box ENGLISH"></span><span>ภาษาอังกฤษ</span>&nbsp;|&nbsp;
            <span class="box DIGIT"></span><span>ตัวเลข</span>&nbsp;|&nbsp;
            <span class="box SPECIAL"></span><span>อักขระพิเศษ</span>&nbsp;|&nbsp;
            <span class="box GROUP"></span><span>เครื่องหมาย</span>&nbsp;
            <hr>
        </div>
        """

        # append data to html
        for i, word in enumerate(results):
            html += '<span class="{}">{}</span>'.format(
                self.typeWord[typeLists[i]], word)
        html += '</body></html>'

        # write html file
        pathOutput = os.path.join(os.environ.get("PATH_OUTPUT"), "{}.html".format(fileName))
        try:
            with codecs.open(pathOutput, 'w', "utf-8") as htmlFile:
                htmlFile.write(html)
        except Exception as e:
            print(e)

    def connectGlexService(self,text,fileName):

        # send text to glex service
        url = self.hostingGlex
        # url = "http://127.0.0.1:8080/glexSegment"

        # text = {"text": "เป็นการจัดกลุ่ม routes ของ request ว่า request ไหนต้องมีการ "}
        text = dict({"text": text})

        # get respone and create html file
        try:
            print(">>> connect glex service")
            response = requests.get(url, params=text)
            # print(">>> respones : ",json.loads(response.text))
            if(response.status_code == 200):
                try:
                    print(">>> status ok : ",response.json())
                    response = json.loads(response.text)
                    # print("-->>>",response)
                    if(len(response['results']) == len(response['typeLists']) and response['status'] =="ok"):
                        results = response['results']
                        typeLists = response['typeLists']
                        formatToStruct = list(zip(response['results'], response['typeLists']))
                        try:
                            # self.creatHTML(results, typeLists,fileName)
                            return {"status": "ok","results":formatToStruct,"fileName":fileName}

                        except Exception as e:
                            return {"status": "failed","message":"can not create html file"}                   
            
                except Exception as e:
                    print(e)
                    return {"status": "failed","message":"can not format json from glex service "}
            else:
                return {"status": "failed","message":"can't connect glex service(status code :{})".format(response.status_code)} 
        except Exception as e:
            print(e)
            return {"status": "failed","message":"can't connect glex service(status code :{})".format(response.status_code)} 



    def glexSeg(self,text,fileName):
        # read file
        # text = readFile(path)
        print(">>> text :",text)
        print(">>> text :",fileName)
        return self.connectGlexService(text,fileName)


    def test(self):
        return {"status": "OK"}


if __name__ == "__main__":
    # from glex import glexSeg
    # glexSeg(self, text,fileName):

    pass
