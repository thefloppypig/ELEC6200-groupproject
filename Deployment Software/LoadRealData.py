import csv
import os
import time
from SensorData import *
from LoadData import sensorToXY

# Load data and return X,y training data
def loadinRealData(root_directory, xOrder):
    sensors = []
    sensors = loadData(sensors, root_directory, "FreezeAttack/", "FreezerAttack")
    sensors = loadData(sensors, root_directory, "HeatAttack/", "HeatAttack")
    sensors = loadData(sensors, root_directory, "OpenLidAttack/", "OpenLidAttack")
    sensors = loadData(sensors, root_directory, "DrillAttack/", "DrillAttack")
    sensors = loadData(sensors, root_directory, "Normal/", "Normal")
    sensors = removeUselessSensors(sensors)
    return sensorToXY(sensors, xOrder)

# Load data into an array contaning SensorData objects
def loadData(sensors, root_directory, directory_name, behaviour):
    # Find files
    directory = root_directory + directory_name
    files = [file for file in os.listdir(directory) if file.endswith(".txt")]

    # Parse every file and create and array with SensorData objects
    for file in files:
        with open(directory + file) as csv_file:
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
                    chunks = line[0].split(',')
                    for entry in chunks:
                        entry = entry.replace(' ', '')
                        sensors[whichSensorData].insertItem(float(entry))
                        whichSensorData = whichSensorData + 1
                i = i+1
    return sensors

# You could flip the if to avoid "continue"
# Not sure what useles sensors are. Check MSc report
def removeUselessSensors(sensors):
    newSensorList = []
    for x in range(0, len(sensors)):
        if ((sensors[x].name == "Altitude" or sensors[x].name == "Core0" or sensors[x].name == "Core1" or sensors[x].name == "Core2" or sensors[x].name == "Core3")):
            continue
        else:
            newSensorList.append(sensors[x])
    return newSensorList
