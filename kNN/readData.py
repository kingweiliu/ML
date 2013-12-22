from numpy import *

def file2Matrix(filename):
    fin = file(filename, 'r')
    arrayOfLines = fin.readlines()
    linesCnt = len(arrayOfLines)
    returnMat = zeros((linesCnt, 3))
    returnLabel = []

    index = 0
    for ln in arrayOfLines:
        line = ln.strip()
        lstFromLine = line.split('\t')
        returnMat[index:] = lstFromLine[0:3]
        returnLabel.append(lstFromLine[-1])
        index +=1
    return returnMat, returnLabel

a=file2Matrix("D:\\github\\ML\\kNN\\datingTestSet.txt")

