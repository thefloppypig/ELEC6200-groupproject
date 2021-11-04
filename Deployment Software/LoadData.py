import csv
import os

from SensorData import SensorData

#Machine Learning Section Init
import pandas as pd
import numpy as np

# Get the type for all sensors[]
def generateXOrder(sensors):
    xOrder = [item.type for item in sensors]
    return list(set(xOrder))

# Load data and return X,y training data
def loadInTrainingData(directory, xOrder):
    files = [file for file in os.listdir(directory) if filename.endswith(".txt")]
    sensors = importData(directory, files)
    return sensorToXY(sensors, xOrder)

# Load all data from the "files" in a "directory"
def importData(directory, files):
    sensors = []
    for file in files:
        with open(directory + file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\n")
            i = 0
            name = ""
            type = ""
            behaviour = ""
            data = []
            time = []
            for line in csv_reader:
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

# Create labelled dataset from sensor readings
def sensorToXY(sensors, xOrder):
    #Find Distinct Behaviours
    behaviours = []
    distinctSensors = []
    for item in sensors:
        behaviours.append(item.behaviour)
        distinctSensors.append(item.name)

    #Makes them distinct
    behaviours = list(set(behaviours))
    distinctSensors = list(set(distinctSensors))

    sensorDataArrays = []
    for item in distinctSensors:
        sensorDataArrays.append([])

    Y = []
    for item in sensors:
        itemIndex = xOrder.index(item.type)
        sensorDataArrays[itemIndex] = np.append(sensorDataArrays[itemIndex], item.data)
        if (itemIndex == 0):
            behaviours.index(item.behaviour)
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
