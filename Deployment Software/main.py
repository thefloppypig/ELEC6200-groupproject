import time
from LoadModels import loadModels
from Sensors import initialiseSensors, pollSensors
import numpy as np

def checkModels(models01, models11, attackClassificationModel, x):
    x = x.reshape(1,-1)

    #model01 means 0 is in and 1 is out
    #model11 means 1 is in and -1 is out
    potentials = []
    for model in models01:
        # If inlier
        if (models01.get(model).predict(x) == 0):
            potentials.append(model)

    for model in models11:
        # If inlier
        if (models11.get(model).predict(x) == 1):
            potentials.append(model)

    #print(len(potentials))
    if (len(potentials) > 1):
        #Overlaps between multiple behaviours
        return attackClassificationModel.predict(x)[0], len(potentials)
    elif (len(potentials) ==  1):
        #Known behaviour
        return potentials[0], 1
    else:
        #Potentially unknown attack
        return "Unknown", 0

# While True
# Read from sensors
# Store input data in data_entry[]
# Feed input data to all models
# Print predictions
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

    models01, models11, attackClassificationModel = loadModels()
    bme280, i2c, tsl1, acc = initialiseSensors()

    while (True):
        start_time = time.time()
        sensor_data = pollSensors(bme280, i2c, tsl1, acc)

        data_entry = []

        for xEntry in xOrder:
            for item in sensor_data:
                if (xEntry == item):
                    data_entry.append(sensor_data.get(item))

        data_entry = np.array(data_entry)
        return_data = checkModels(models01, models11, attackClassificationModel, data_entry)
        end_time = time.time()
        print(return_data)

if __name__ == "__main__":
    main()
