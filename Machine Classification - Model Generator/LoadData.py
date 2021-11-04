import csv
import os
import numpy as np

from SensorData import SensorData

def loadInTrainingData(directory, xOrder):
    sensors = getSensorData(directory)
    return sensorToXY(sensors, xOrder)

def generateXOrder(sensors):
    xOrder = []
    for item in sensors:
        xOrder.append(item.type)
    xOrder = list(set(xOrder))
    return xOrder

def getSensorData(directory):
    files = findFiles(directory)
    return importData(directory, files)

def sensorToXY(sensors, xOrder):
    behaviours, distinctSensors = calculateDistinctSensorsAndBehaviours(sensors)
    X, y  = convertSensorArrayIntoXYFormat(sensors, behaviours, distinctSensors, xOrder)
    return X, y

def findFiles(directory):
    #Finds all the files that need loading in
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            files.append(filename)
    return files

def importData(directory, files):
    #Loads in all the data
    sensors = []
    for file in files:
        with open(directory + file) as csv_file:
            #print (file)
            csv_reader = csv.reader(csv_file, delimiter="\n")
            i = 0
            name = ""
            type = ""
            behaviour = ""
            data = []
            time = []
            for line in csv_reader:
                #print(file, line)
                if (i == 0):
                    name = line[0]
                elif (i == 1):
                    type = line[0]
                elif (i == 2):
                    behaviour = line[0]
                else:
                    data.append(line)
                    time.append(i-3)
                i = i + 1
            sensors.append(SensorData(name, type, behaviour, data, time))
    return sensors

def calculateDistinctSensorsAndBehaviours(sensors):
    #Find Distinct Behaviours
    behaviours = []
    distinctSensors = []
    for item in sensors:
        behaviours.append(item.behaviour)
        distinctSensors.append(item.name)

    #Makes them distinct
    behaviours = list(set(behaviours))
    distinctSensors = list(set(distinctSensors))
    return behaviours, distinctSensors

def convertSensorArrayIntoXYFormat(sensors, behaviours, distinctSensors, xOrder):
    sensorDataArrays = []
    for item in distinctSensors:
        sensorDataArrays.append([])

    Y = []
    for item in sensors:
        itemIndex = xOrder.index(item.type)
        sensorDataArrays[itemIndex] = np.append(sensorDataArrays[itemIndex], item.data)
        if (itemIndex == 0):
            catVal = behaviours.index(item.behaviour)
            for x in range(0, len(item.data)):
                Y.append(item.behaviour)

    xOrder = []
    for entry in distinctSensors:
        for sensor in sensors:
            if (entry == sensor.name and sensor.behaviour == behaviours[0]):
                xOrder.append(sensor.type)

    sensorDataArraysnp = np.array([sensorDataArrays[0]])
    sensorDataArrays.pop(0)
    for item in sensorDataArrays:
        sensorDataArraysnp = np.dstack((sensorDataArraysnp, np.array(item)))

    sensorDataArraysnp = sensorDataArraysnp[0]
    data = sensorDataArraysnp

    X = data
    X = X.astype(np.float)
    y = Y

    return X, y
