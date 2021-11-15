import csv
import os

from SensorData import SensorData
from LoadData import calculateDistinctSensorsAndBehaviours, convertSensorArrayIntoXYFormat

def loadinRealData(directory, xOrder):
    sensors = []
    sensors = loadData(sensors, directory, "FreezeAttack/", "FreezerAttack")
    sensors = loadData(sensors, directory, "HeatAttack/", "HeatAttack")
    sensors = loadData(sensors, directory, "OpenLidAttack/", "OpenLidAttack")
    sensors = loadData(sensors, directory, "DrillAttack/", "DrillAttack")
    sensors = loadData(sensors, directory, "Normal/", "Normal")
    sensors = removeUselessSensors(sensors)
    behaviours, distinctSensors = calculateDistinctSensorsAndBehaviours(sensors)
    X, y  = convertSensorArrayIntoXYFormat(sensors, behaviours, distinctSensors, xOrder)
    return X, y

def findFiles(directory, directoryName):
    directory = directory + directoryName
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            files.append(filename)
    return files

def loadData(sensors, directory, directoryName, behaviour):
    files = findFiles(directory, directoryName)
    for file in files:
        with open(directory + directoryName + file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\n")
            i = 0
            numberOfSensorsInThisFile = 0

            for line in csv_reader:
                whichSensorData = len(sensors) - numberOfSensorsInThisFile
                if (i == 0):
                    chunks = line[0].split(',')
                    for entry in chunks:
                        entry = entry.replace(' ', '')
                        sensors.append(SensorData(entry, entry, behaviour, [], []))
                        numberOfSensorsInThisFile = numberOfSensorsInThisFile + 1
                else:
                    #print(len(line))
                    chunks = line[0].split(',')
                    for entry in chunks:
                        entry = entry.replace(' ', '')
                        sensors[whichSensorData].insertItem(float(entry))
                        whichSensorData = whichSensorData + 1
                i = i + 1
    return sensors

def removeUselessSensors(sensors):
    newSensorList = []
    for x in range(0, len(sensors)):
        if ((sensors[x].name == "Altitude" or sensors[x].name == "Core0" or sensors[x].name == "Core1" or sensors[x].name == "Core2" or sensors[x].name == "Core3")):
            continue
            #print(sensors[x].name)
        else:
            #print(sensors[x].name)
            newSensorList.append(sensors[x])
    return newSensorList
