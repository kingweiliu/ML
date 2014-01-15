# -*- coding: cp936 -*-

from numpy import *

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec

def createVocabList(dataSet):
    vocabSet = set([])
    for doc in dataSet:
        vocabSet = vocabSet | set(doc)
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]* len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word: %s is not in my vocabulary!" % word
    return returnVec

def trainNB0(trainMatrix, trainCategory):
    #输入是训练的数据数值化之后的矩阵, 每一列对应了一个单词 
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/ p1Denom)
    p0Vect = log(p0Num/p0Denom)
    return p1Vect, p0Vect, pAbusive #类一的概率矢量, 类0的概率矢量, 类一的概率

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1>p0:
        return 1
    else:
        return 0

def testingNB():
    lstPosts , lstCls = loadDataSet()
    myVocabList = createVocabList(lstPosts)
    trainMat = []
    for post in lstPosts:
        trainMat.append(setOfWords2Vec(myVocabList, post))
    p0v, p1v, pAb = trainNB0(trainMat, lstCls)
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = setOfWords2Vec(myVocabList, testEntry)
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0v, p1v, pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = setOfWords2Vec(myVocabList, testEntry)
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0v, p1v, pAb)



testingNB()


    
    


trainData, trainCls = loadDataSet()
vocabList = createVocabList(trainData)
print vocabList

trainMat= []
for i in range(len(trainData)):
    trainLine = setOfWords2Vec(vocabList, trainData[i])
    trainMat.append(trainLine)
    print trainLine

for i in range(len(trainMat)):
    str = ""
    for j in range(len(trainMat[i])):
        if trainMat[i][j] != 0 :
            str = str + vocabList[j] +"\t"
    print str


print trainNB0(trainMat, trainCls)
