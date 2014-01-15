from numpy import *
import operator

def classify0(inX, dataSet, labels, k):
	dataCnt = dataSet.shape[0]
	diffData = tile(inX, (dataCnt, 1)) - dataSet
	sqrtData = diffData ** 2
	sqDistance = sqrtData.sum(axis=1)
	indexSort = sqDistance.argsort()
	category = {}
	for i in range(k):
		 vLabel = labels[indexSort[i]]
		 category[vLabel] = category.get(vLabel, 0) +1
	sortedCat = sorted(category.iteritems(), key = operator.itemgetter(1), reverse = True)
	return sortedCat[0][0]
