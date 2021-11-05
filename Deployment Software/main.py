import time

from numpy.core.numeric import Infinity
from LoadModels import loadModels
from Sensors import initialiseSensors, pollSensors
from FakeSensors import loadFakeSensorData, pollFakeSensors
import numpy as np
import argparse

# Takes in the models and input 'x'
# returns the tuple containing the predicted attack
def checkModels(models01, models11, attackClassificationModel, x):
    x = x.reshape(1,-1)

    #model01 means 0 is in and 1 is out
    #model11 means 1 is in and -1 is out
    potentials = []
    for model in models01:
        # If inlier
        prediction = models01.get(model).predict(x)
        # print(str(model) + "01 Prediction: " + str(prediction))
        if (prediction == 0):
            potentials.append(model)

    for model in models11:
        # If inlier
        prediction = models11.get(model).predict(x)
        # print(str(model) + "11 Prediction: " + str(prediction))
        if (prediction == 1):
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
def main(sensors_connected=True):
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

    # Load the sensors as normal, only use fake sensors if specified
    attack = "DrillAttack"
    bme280, i2c, tsl1, acc = None, None, None, None if not sensors_connected else initialiseSensors()
    sensor_data_from_files, lines = None, Infinity 
    if (not sensors_connected): 
        sensor_data_from_files, lines = loadFakeSensorData(attack,False)
    models01, models11, attackClassificationModel = loadModels()

    current_line = 0
    sampling_rate = 10
    true_positive = 0
    no_unknown = 0
    round = 0
    all_results = []
    while (current_line < lines):
        # Monitoring sensors begins
        # time.sleep(0.1)
        # print("-------------------------")
        start_time = time.time()

        # Get data from the sensors
        sensor_data = pollSensors(bme280, i2c, tsl1, acc) if sensors_connected else pollFakeSensors(sensor_data_from_files, current_line)
        current_line = current_line + sampling_rate

        data_entry = []
        for xEntry in xOrder:
            for item in sensor_data:
                if (xEntry == item):
                    data_entry.append(sensor_data.get(item))

        data_entry = np.array(data_entry)
        # Send Data to the models for classification
        return_data, potentials = checkModels(models01, models11, attackClassificationModel, data_entry)
        end_time = time.time()
        round = round + 1
        all_results.append(return_data)

        if (str(return_data) == attack):
            true_positive = true_positive + 1
        print("Output: "+ return_data + " | Expected: " + attack + " | Processing Time: " + str(end_time-start_time))
    print("Accuracy: "+str(true_positive/round) + " | " + str(true_positive) + "/" + str(round))
    print("Number of Normal: "+ str(all_results.count("Normal")))
    print("Number of Unknowns: "+ str(all_results.count("Unknown")))
    print("Number of HeatAttack: "+ str(all_results.count("HeatAttack")))
    print("Number of DrillAttack: "+ str(all_results.count("DrillAttack")))
    print("Number of FreezerAttack: "+ str(all_results.count("FreezerAttack")))
    print("Number of OpenLidAttack: "+ str(all_results.count("OpenLidAttack")))


if __name__ == "__main__":
    # Argument parser to add options and descriptions in when using 'main.py --help'
    parser = argparse.ArgumentParser(description='Deployment script of the energy efficient tamper attack detection and response mechanisms')
    parser.add_argument("-n","--nosensors", action='store_true', help="Use this option when no sensors are connected. Uses previously recorded sensor data as input.")
    args = parser.parse_args()
    # Start the main program with the arguments specified
    main(not args.nosensors)
