import pandas as pd

class Frequency():
    def __init__(self):
        pass
    
    def frequencyWord(self,files,typeFile,librarySegment,glexDict):
        df = pd.read_json ('E:\python\glex-service-python\demo/resultDataFrame.json')
        # ผลลัพธ์อาจมีมากกว่า 2 ไฟล์
        result = [("file name1",df.to_csv(index=False),df.to_csv(index=False)),("file name2",df.to_csv(index=False),df.to_csv(index=False))]
        return result