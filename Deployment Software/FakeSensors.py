# This file is only used when running main.py with the '-w' flag
# This provides sensor data to the machine learning algorithm without having any sensors attached

from datetime import datetime
from random import randrange
from os import listdir
from LoadData import importData
from LoadRealData import loadinRealData
import pandas as pd

from ISStreamer.Streamer import Streamer

# Load the sensor data into a data structure which can be given easily to the machine learning algorithm
def loadFakeSensorData(attack="Normal", use_training_data=True):
    data_from_file = {}
    if (use_training_data):
        # Retrieve Data
        directory = "/home/pi/Downloads/project-master/data/testdata/" + attack +"/" #folder which the sensor data is taken from
        imported_data = importData(directory,[file for file in listdir(directory) if file.endswith(".txt")])
        # Format data
        for sensor_data in imported_data:
            if (sensor_data.behaviour == attack):
                data_from_file[sensor_data.type] = sensor_data.data
                
    else:
        print("Loading from: /home/pi/Downloads/project-master/data/realdata/" + attack + "/")
        # Retrieve Data
        directory = "/home/pi/Downloads/project-master/data/realdata/" + attack + "/" #folder which the sensor data is taken from
        csv_data = [pd.read_csv(directory+file, sep=",", header=0) for file in listdir(directory) if file.endswith(".txt")]
        # Format Data
        for csv in csv_data:
            titles = csv.columns
            for title in titles:
                data_from_file[title.strip()] = csv[title].to_numpy()
    lines = len(data_from_file['Lux'])
    print("Fake Sensor data has been loaded. Total sensor variables: "+str(len(data_from_file))+ " | Lines in file: " + str(lines))
    return data_from_file, lines




# Return a random row of data from the data structure given in the parameter
def pollFakeSensors(data_from_file, i):
	sensorData = {}
	row_number = i #randrange(len(data_from_file['Lux']))

    #Light sensor
	sensorData['Lux'] = data_from_file['Lux'][row_number]
	sensorData['Infrared'] = data_from_file['Infrared'][row_number]
	sensorData['Visible'] = data_from_file['Visible'][row_number]
	sensorData['Full_Spectrum'] = data_from_file['Full_Spectrum'][row_number]
	sensorData['Accelerometer_x_axis'] = data_from_file['Accelerometer_x_axis'][row_number]
	sensorData['Accelerometer_y_axis'] = data_from_file['Accelerometer_y_axis'][row_number]
	sensorData['Accelerometer_z_axis'] = data_from_file['Accelerometer_z_axis'][row_number]

	#BME280
	sensorData['Temperature'] = data_from_file['Temperature'][row_number]
	sensorData['Humidity'] = data_from_file['Humidity'][row_number]
	sensorData['Pressure'] = data_from_file['Pressure'][row_number]

	#Core Usage
	sensorData['All_Cores'] = data_from_file['All_Cores'][row_number]
	print("Input: "+str(sensorData))
	return sensorData
