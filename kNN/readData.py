from numpy import *

def file2Matrix(filename):
    fin = file(filename, 'r')
    arrayOfLines = fin.readlines()
    linesCnt = len(arrayOfLines)
    returnMat = zeros((linesCnt, 3))
    returnLabel = []

    index = 0

    labelIndex = 1
    labelMap ={}

    for ln in arrayOfLines:
        line = ln.strip()
        lstFromLine = line.split('\t')
        returnMat[index:] = lstFromLine[0:3]
        lb = lstFromLine[-1]
        lbNumber = 0
        if labelMap.has_key(lb):
            lbNumber = labelMap[lb]
        else:
            lbNumber = labelIndex
            labelMap[lb] = labelIndex
            labelIndex = labelIndex +1
        returnLabel.append(lbNumber)
        index +=1
    return returnMat, returnLabel

def autoNorm(dataSet):
    minVal = dataSet.min(0)
    maxVal = dataSet.max(0)
    ranges = maxVal - minVal
    row = dataSet.shape[0]
    normDataSet = dataSet - tile(minVal, (row, 1))
    normDataSet = normDataSet / tile(ranges, (row, 1))
    return normDataSet, ranges, minVal

a, b=file2Matrix("datingTestSet.txt")
import kNN

a, ranges, minVals = autoNorm(a)
errorCnt  = 0
allCnt = a.shape[0]
tstCnt = int(allCnt*0.5)
for i in range(tstCnt):
    cls = kNN.classify0(a[i, :], a[tstCnt:allCnt, :], b[tstCnt:allCnt], 3)
    if cls != b[i]:
        errorCnt = errorCnt + 1
        
print errorCnt / float(tstCnt)
print errorCnt
    

#a, c, d = autoNorm(a)
#import matplotlib
#import matplotlib.pyplot as plt
#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.scatter(a[:, 1], a[:,0], 15* array(b), 15* array(b))
#plt.show()
