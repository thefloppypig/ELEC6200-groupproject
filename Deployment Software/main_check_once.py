from time import time, sleep
from numpy.core.numeric import Infinity, array
from pandas import DataFrame
from config import *
from datetime import datetime
from LoadModels import loadModels
from Sensors import initialiseSensors, pollSensors
from Response import *

def checkModels(models01, models11, attackClassificationModel, x):
    x = x.reshape(1,-1)
    potentials = []
    for model in models01:
        prediction = models01.get(model).predict(x)
        if (prediction == 0):
            potentials.append(model)
    for model in models11:
        prediction = models11.get(model).predict(x)
        if (prediction == 1):
            potentials.append(model)

    if (len(potentials) > 1):
        return attackClassificationModel.predict(x)[0], len(potentials)
    elif (len(potentials) ==  1):
        return potentials[0], 1
    else:
        return "Unknown", 0

def main():
    xOrder =['Lux',
    'Infrared',
    'Visible',
    'Full_Spectrum',
    'Temperature',
    'Humidity',
    'Pressure',
    'Accelerometer_x_axis',
    'Accelerometer_y_axis',
    'Accelerometer_z_axis',
    'All_Cores']

    # Init sensors and get data from them
    bme280, i2c, tsl1, acc = initialiseSensors()
    sensor_data = pollSensors(bme280, i2c, tsl1, acc) 

    # Load models
    models01, models11, attackClassificationModel = loadModels()

    # Prepare input for model
    data_entry = []
    for xEntry in xOrder:
        for item in sensor_data:
            if (xEntry == item):
                data_entry.append(sensor_data.get(item))
    data_entry = array(data_entry)

    # Check
    return_data, potentials = checkModels(models01, models11, attackClassificationModel, data_entry)
    print(return_data)

# This is run first
if __name__ == "__main__":
    main()