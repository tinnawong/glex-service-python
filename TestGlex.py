import unittest
from demo.glex.glex import Glex
from demo import app
from demo import views
from flask import request, jsonify
import json
import codecs
from werkzeug.datastructures import FileStorage


class TestGlex(unittest.TestCase):
    glex = Glex()

    # test method in service
    def test_viewsAllowed(self):
        self.assertTrue(views.allowed_file("tesxt.txt"))
        self.assertFalse(views.allowed_file("tesxt.doc"))

    def test_viewsGetNameFile(self):
        self.assertEqual(views.getNameFile("test-2 3.txt"), "test-2 3")

    # test service
    def test_connectGlexService(self):
        text = "นำรถมาประเมินราคายังจุดนัดหมายของ Carsome อันดับ 7 คำถามฮิต 7 ข้อเกี่ยวกับคินเดิลกูเกิล จึงปรากฏบทความของผมอยู่ในอันดับต้นๆ [--*] {-*/}|"
        fileName = "test"
        response = "{'status': 'ok', 'results': [('นำ', 1), ('รถ', 1), ('มา', 1), ('ประเมินราคา', 2), ('ยัง', 1), ('จุด', 2), ('นัดหมาย', 2), ('ของ', 2), (' ', 5), ('Carsome', 3), (' ', 5), ('อันดับ', 2), (' ', 5), ('7', 4), (' ', 5), ('คำถาม', 2), ('ฮิต', 1), (' ', 5), ('7', 4), (' ', 5), ('ข้อ', 1), ('เกี่ยวกับ', 2), ('คินเดิลกู', 0), ('เกิล', 0), (' ', 5), ('จึง', 1), ('ปรากฏ', 2), ('บทความ', 2), ('ของ', 2), ('ผม', 1), ('อยู่', 1), ('ใน', 1), ('อันดับ', 2), ('ต้น', 1), ('ๆ', 0), (' ', 5), ('[--*]', 6), (' ', 5), ('{', 5), ('-', 5), ('*', 5), ('/', 5), ('}', 5), ('|', 5)], 'fileName': 'test'}"
        self.assertEqual(
            str(self.glex.connectGlexService(text, fileName)).replace(" ", ""), response.replace(" ", ""),"Please start glex service (go server)")

    def test_pingMainService(self):
        with app.test_client() as c:
            resp = c.get('/ping')
            data = json.loads(resp.data)
            self.assertTrue(data['status'] == "ok")

    def test_SegmentMainService(self):
        with app.test_client() as c:
            my_file = FileStorage(
                stream=open("./fileTest.txt", "rb"),
            ),
            resp = c.get(
                "/glexSegment",
                data={
                    "file": my_file,
                },
                content_type="multipart/form-data"
            )
            data = json.loads(resp.data)
            self.assertTrue(data['status'] == "ok","please check glex service make sure started")


if __name__ == '__main__':
    unittest.main()