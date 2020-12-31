#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
import pandas as pd
import deepcut
from pythainlp.util import rank
import tltk
from collections import Counter
from pythainlp import word_tokenize
import csv
import time

class frequencyWordExpotcsv():


    def __init__(self,TupleFile=None,Filetype=None,LibraryNumber=None,selectSystem=None,Dictname=None,Foldername=None):
        
        self.TupleFile = TupleFile
        self.Filetype = Filetype
        self.LibraryNumber = LibraryNumber
        self.selectSystem = selectSystem
        self.Dictname = Dictname
        self.Foldername = Foldername
        self.TextListFolder = []
        self.resultData = []

    

    def setText(self,TextFile):
        
        if(self.Filetype == 'raw'):
            TextList = TextFile.replace(" ", "")
            self.TextListFolder.append(TextList)
        elif(self.Filetype == 'pipe'):
            TextList = TextFile.replace("|", "")
            self.TextListFolder.append(TextList)
        elif(self.Filetype == 'line'):
            TextList = TextFile.replace("\n", "")
            self.TextListFolder.append(TextList)
        else:
            print('Error File Type')
        return TextList ,self.TextListFolder

    def selectLibraryFile(self,TextList):
        if self.LibraryNumber == 'glex':
            Key = {'text':TextList, 'useDict':self.Dictname}
            TextResponse = requests.get('http://127.0.0.1:8080/glex/segment', Key)
            cutWords = TextResponse.json()['results']
        elif self.LibraryNumber == 'deepcut':
            cutWords = deepcut.tokenize(TextList)
        elif self.LibraryNumber == 'tltk':
            cutWords = tltk.nlp.word_segment(TextList).split('|')
        elif self.LibraryNumber == 'newmm':
            cutWords = word_tokenize(TextList, engine='newmm')
        elif self.LibraryNumber =='mm':
            cutWords = word_tokenize(TextList, engine='mm')
        return cutWords

    def selectLibraryFolder(self):
        TextListFile = ''.join(self.TextListFolder)
        if self.LibraryNumber == 'glex':
            Key = {'text':TextListFile, 'useDict':self.Dictname}
            TextResponse = requests.get('http://127.0.0.1:8080/glex/segment', Key)
            cutWords = TextResponse.json()['results']
        elif self.LibraryNumber == 'deepcut':
            cutWords = deepcut.tokenize(TextListFile)
        elif self.LibraryNumber == 'tltk':
            cutWords = tltk.nlp.word_segment(TextListFile).split('|')
        elif self.LibraryNumber == 'newmm':
            cutWords = word_tokenize(TextListFile, engine='newmm')
        elif self.LibraryNumber =='mm':
            cutWords = word_tokenize(TextListFile, engine='mm')
        return cutWords
    
    def lenWords(self,cutWords):
        Words = len(cutWords)
        return Words
    
    def getUniqueWords(self,cutWords):
        uniqueWords = len(Counter(cutWords))
        return uniqueWords

    def repeatWords(self,cutWords):
        WordsRepeat = rank(cutWords)
        return WordsRepeat

    def exportCSV(self,Words,uniqueWords,WordsRepeat,NameFile):
        
        DataSummary = {
            'จำนวนคำทั้งหมด':Words,
            'จำนวนคำที่ไม่ซ้ำทั้งหมด':uniqueWords,
            'ระบบในการตัดคำ':self.LibraryNumber,
            'เวลา':time.strftime('%d-%m-%Y %H:%M:%S')}

        DataFrequencyCSV = pd.DataFrame(WordsRepeat.most_common(), columns=['รายการคำ','ความถี่ของคำ'])
        DataSummaryCSV = pd.DataFrame({key:pd.Series(value) for key, value in DataSummary.items()})
        resultDataSummaryCSV = DataSummaryCSV.to_csv(index=False,encoding='utf-8-sig')
        resultDataFrequencyCSV = DataFrequencyCSV.to_csv(index=False,encoding='utf-8-sig')
        return ('(สรุปจำนวนคำ)'+NameFile,resultDataFrequencyCSV),('(ความถี่คำ)'+NameFile,resultDataSummaryCSV)
    
    def frequencyWordExpotCSVFile(self):
        for NameFile,TextFile in self.TupleFile:
            TextList,self.TextListFolder = self.setText(TextFile)
            cutWords = self.selectLibraryFile(TextList)
            Words = self.lenWords(cutWords)
            WordsRepeat = self.repeatWords(cutWords)
            uniqueWords = self.getUniqueWords(cutWords)
            resultDataFrequencyCSV, resultDataSummaryCSV = self.exportCSV(Words,uniqueWords,WordsRepeat,NameFile)
            self.resultData.append(resultDataFrequencyCSV)
            self.resultData.append(resultDataSummaryCSV)

    def frequencyWordExpotCSVFolder(self):
        
        for NameFile,TextFile in self.TupleFile:
            TextList,self.TextListFolder = self.setText(TextFile)
        cutWords = self.selectLibraryFolder()
        Words = self.lenWords(cutWords)
        WordsRepeat = self.repeatWords(cutWords)
        uniqueWords = self.getUniqueWords(cutWords)
        NameFile = self.Foldername
        resultDataFrequencyCSV, resultDataSummaryCSV = self.exportCSV(Words,uniqueWords,WordsRepeat,NameFile)
        self.resultData.append(resultDataFrequencyCSV)
        self.resultData.append(resultDataSummaryCSV)
        
    

    def systemfrequencyWordExpotCSV(self):
        if(self.selectSystem == 'fileandfolder'):
            self.frequencyWordExpotCSVFolder()
            self.frequencyWordExpotCSVFile()
        elif(self.selectSystem == 'folder'):
            self.frequencyWordExpotCSVFolder()
        elif(self.selectSystem == 'file'):
            self.frequencyWordExpotCSVFile()
        else:
            print('Error frequencyWordExpotCSV')
        return self.resultData

if __name__ == "__main__":
    pass
