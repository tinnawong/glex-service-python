import unittest
from app.glex.glex import Glex
from app import app
from app import routes
from flask import request, jsonify
import json
import codecs
from werkzeug.datastructures import FileStorage


class TestGlex(unittest.TestCase):
    glex = Glex()

    # test method in service
    def test_viewsAllowed(self):
        self.assertTrue(routes.allowedFile("tesxt.txt"))
        self.assertFalse(routes.allowedFile("tesxt.doc"))

    def test_viewsGetNameFile(self):
        self.assertEqual(routes.getNameFile("test-2 3.txt"), "test-2 3")
        self.assertEqual(routes.getNameFile("test-2/*. 3.txt"), "test-2/*. 3")

    # test service
    def test_connectGlexService(self):
        text = "นำรถมาประเมินราคา1000 [--*] {-*/}|"
        fileName = "test"
        response = "{'status':'ok','results':[('นำ',1),('รถ',1),('มา',1),('ประเมินราคา',2),('1000',4),('',5),('[--*]',6),('',5),('{',5),('-',5),('*',5),('/',5),('}',5),('|',5)],'fileName':'test','dictName':'lexitron.txt'}"
        self.assertEqual(
            str(self.glex.connectGlexService(text, fileName)).replace(" ", ""), response.replace(" ", ""),"Please check respone or check status glex service (go server)")

    def test_pingMainService(self):
        with app.test_client() as c:
            resp = c.get('/ping')
            data = json.loads(resp.data)
            self.assertTrue(data['status'] == "ok")

    def test_SegmentMainService(self):
        with app.test_client() as c:
            my_file = FileStorage(
                stream=open("fileTest.txt", "rb"),
            ),
            resp = c.get(
                "/glexSegment",
                data={
                    "file": my_file,
                },
                content_type="multipart/form-data"
            )
            respones = json.loads(resp.data)
            assumpResults = [['ทดสอบ', 2], ['การ', 2], ['ตัด', 1], ['123', 4], [' ', 5], ['/', 5], ['*', 5], ['-', 5], [' ', 5], ['test', 3], [' ', 5], ['[+-\\]', 6]]
            self.assertTrue(respones['status'] == "ok","please check glex service make sure started")
            self.assertEqual(assumpResults,respones['results'])
            self.assertTrue(respones['dictName'])



if __name__ == '__main__':
    unittest.main()