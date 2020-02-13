#script for discovering the best number of attributes

import numpy as np
from sklearn import linear_model
from math import sqrt
import matplotlib.pyplot as plot
from xattrSelect import xattrSelect


def best_num_attr(xList, xListTrain, xListTest, labelsTrain, labelsTest):
    #build list of attributes one-at-a-time - starting with empty
    attributeList = []
    index = range(len(xList[1]))
    indexSet = set(index)
    indexSeq = []
    oosError = []

    for i in index:
        attSet = set(attributeList) #set creates a list of unordered collection of unique items
        #attributes not in list already
        attTrySet = indexSet - attSet
        #form into list
        attTry = [ii for ii in attTrySet]
        errorList = []
        attTemp = []
        #try each attribute not in set to see which
        #one gives least oos error
        for iTry in attTry:
            attTemp = [] + attributeList
            attTemp.append(iTry)
            #use attTemp to form training and testing sub matrices
            #as list of lists
            xTrainTemp = xattrSelect(xListTrain, attTemp)
            xTestTemp = xattrSelect(xListTest, attTemp)
            #form into np arrays
            xTrain = np.array(xTrainTemp)
            yTrain = np.array(labelsTrain)
            xTest = np.array(xTestTemp)
            yTest = np.array(labelsTest)
            #use sci-kit learn linear regression
            wineQModel = linear_model.LinearRegression()
            wineQModel.fit(xTrain,yTrain)
            #use trained model to generate prediction and calculate rmsError
            rmsError = np.linalg.norm((yTest-wineQModel.predict(xTest)),2)/sqrt(len(yTest))
            errorList.append(rmsError)
            attTemp = []
        iBest = np.argmin(errorList)
        attributeList.append(attTry[iBest])
        oosError.append(errorList[iBest])
    print("Out of sample error versus attribute set size" )
    print(oosError)
    print("\n" + "Best attribute indices")
    print(attributeList)

#    namesList = [names[i] for i in attributeList]
#    print("\n" + "Best attribute names")
#    print(namesList)

    #Plot error versus number of attributes
    x = range(len(oosError))
    plot.plot(x, oosError, 'k')
    plot.xlabel('Number of Attributes')
    plot.ylabel('Error (RMS)')
    plot.show()
  