import csv
import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.svm import SVC
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
import time

def make_meshgrid(x, y, h=.02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    return xx, yy

def plot_contours(clf, xx, yy):
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    #print(time.time() - startTime)
    Z = Z.reshape(xx.shape)
    #print(time.time() - startTime)
    #out = ax.contourf(xx, yy, Z, **params)
    return Z

def generateGraphDataTotal(X, clf, title):
    xx, yy, contourPlot = generateGraphData(X, clf)
    displayGraphData(xx, yy, X, contourPlot, title)

def generateGraphData(X, clf):
    # Set-up grid for plotting.
    X0, X1 = X[:, 0], X[:, 1]
    print (len(X0), len(X1))
    print (X0[0])
    xx, yy = make_meshgrid(X0, X1)
    contourOutput = plot_contours(clf, xx, yy)
    return xx, yy, contourOutput

def displayGraphData(xx, yy, X, contourOutput, name):
    #Plot Data
    fig, ax = plt.subplots(figsize=(15,15))
    X0, X1 = X[:, 0], X[:, 1]
    # title for the plots
    title = (name)

    ax.contourf(xx, yy, contourOutput, cmap=plt.cm.coolwarm, alpha=0.25)
    ax.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, alpha=0.5)
    ax.set_title(title)
    plt.draw()

def outputVerificationGraph(data, y, behaviours, distinctSensors):
    plt.figure(figsize=(15,15))
    distinctY = list(set(y))
    print(distinctY)
    area = np.pi*3
    data = data.astype(np.float)
    x1, x2 = data[:, 0], data[:, 1]
    for catY in distinctY:
        printData1 = []
        printData2 = []
        i = -1
        for item in x1:
            i = i + 1
            if (y[i] == catY):
                printData1.append(x1[i])
                printData2.append(x2[i])
        print(catY, " Done")
        plt.scatter(printData1, printData2, s=20, label=behaviours[catY], cmap=plt.cm.coolwarm, alpha=0.5)

    plt.title('Normal & Attack Data (for the first two sensors)')
    plt.xlabel(distinctSensors[0])
    plt.ylabel(distinctSensors[1])
    plt.legend()
    plt.draw()
    plt.show()
