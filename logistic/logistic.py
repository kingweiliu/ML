from pylab import *

def loadData():
    f = file('testSet.txt')
    matX = []
    matY = []
    cls = []
    for ln in f.readlines():
        datas = ln.split()
        matX.append(float(datas[0]))
        matY.append(float(datas[1]))
        cls.append(int(datas[2]))
    return matX, matY, cls

def drawPnts(x, y, cls):
    pxA = []
    pyA=[]
    pxB=[]
    pyB=[]
    for i in range(len(x)):
        if cls[i] == 0:
            pxA.append(x[i])
            pyA.append(y[i])
        else:
            pxB.append(x[i])
            pyB.append(y[i])    
    scatter(pxA, pyA, s=20, c='r', marker='*')
    scatter(pxB, pyB)
    show()






x, y, cls = loadData()
drawPnts(x, y, cls)
