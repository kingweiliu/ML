import matplotlib
import matplotlib.pyplot
import numpy
import random

def LoadData():
    f = file('ruspini.txt')
    dataSet = []    
    for ln in f.readlines():
        if ln[0] != '#':
            ds = ln.split()
            dataSet.append([int(ds[0]), int(ds[1])])
    return numpy.array(dataSet)

def drawData(ds, cls=[]):
    dsMat = ds
    clsMarker = "*o<+"
    if len(cls)==0:
        matplotlib.pyplot.scatter(dsMat[:, 0], dsMat[:, 1], marker='<', color='r')
    else:
        for i in range(len(cls)):
            matplotlib.pyplot.scatter(dsMat[i, 0], dsMat[i, 1], marker=clsMarker[cls[i]])        
    matplotlib.pyplot.show()
    

def kMeans(ds, k):    
    kMeans = random.sample(ds, k)        
    nShape = ds.shape
    errorSum = 100
    while errorSum > 1:
        kMeansNext = numpy.zeros((4, 2))
        cls = []
        for j in range(nShape[0]):
            pnt = numpy.tile(ds[j, :], (k, 1))
            kError = numpy.sum((kMeans - pnt)**2, axis=1)
            clsIndex = kError.argmin()
            cls.append(clsIndex)
            kMeansNext[clsIndex] = kMeansNext[clsIndex] + ds[j, :]            
        clsCnt = numpy.bincount(cls)
        drawData(ds, cls)              
        kMeansNext = kMeansNext / numpy.tile(clsCnt.transpose(), (2, 1)).transpose()
        print kMeansNext
        errorSum = numpy.sum((kMeans - kMeansNext)**2)
        kMeans = kMeansNext
    return cls

ds = LoadData()
drawData(ds)
kMeans(ds, 4)



    
