import time

from numpy.core.numeric import Infinity
from LoadModels import loadModels
from Sensors import initialiseSensors, pollSensors
from FakeSensors import loadFakeSensorData, pollFakeSensors
import numpy as np
import argparse
import pandas as pd
import os
from datetime import datetime


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
    attack = "Normal"
    bme280, i2c, tsl1, acc = None, None, None, None if not sensors_connected else initialiseSensors()
    sensor_data_from_files, lines = None, Infinity 
    if (not sensors_connected): 
        sensor_data_from_files, lines = loadFakeSensorData(attack,False)
    models01, models11, attackClassificationModel = loadModels()

    current_line = 0
    sampling_rate = 10
    true_positive = 0
    round = 0
    saved_results = []
    saved_sensor_data = []
    potential_attacks = 0
    level_1 = True
    sleep_count = 0
    while (current_line < lines):
        # Monitoring sensors begins
        start_time = time.time()
        if potential_attacks < 3:
            level_1 = True
            time.sleep(3)
            sampling_rate = 3
        else:
            level_1 = False
            time.sleep(1)
            sampling_rate = 1
        # print("-------------------------")

        # Get data from the sensors
        sensor_data = pollSensors(bme280, i2c, tsl1, acc) if sensors_connected else pollFakeSensors(sensor_data_from_files, current_line)
        current_line = current_line + sampling_rate
        # Format Data to be sent into the models
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
        saved_results.append(return_data)
        saved_sensor_data.append(sensor_data)

        # Count detected attacks
        if return_data != "Normal": # If there is an attack
            potential_attacks = potential_attacks + 1
            sleep_count = 0
            reset_count = 0
        elif not level_1: # If in level 2 and no attack detected
            reset_count = reset_count + 1
            potential_attacks = 0
            if reset_count > 4: # No attacks when in level 2 for a long time, reset to level 1
                level_1 = True
                sleep_count = 0
        elif level_1: # If in level 1 and no attack detected
            sleep_count = sleep_count + 1
            if sleep_count > 10:
                goToSleep()
                return

        # Trigger Defense
        if potential_attacks == 3:
            defenseLevel1(return_data)
        if potential_attacks == 4:
            defenseLevel2(return_data, saved_sensor_data, xOrder)
            return

        # Output 
        if (str(return_data) == attack):
            true_positive = true_positive + 1
        print("Output: "+ return_data + " | Expected: " + attack + " | Processing Time: " + str(end_time-start_time))

    # Summary of output after while loop completes
    print("Accuracy: "+str(true_positive/round) + " | " + str(true_positive) + "/" + str(round))
    print("Number of Normal: "+ str(saved_results.count("Normal")))
    print("Number of Unknowns: "+ str(saved_results.count("Unknown")))
    print("Number of HeatAttack: "+ str(saved_results.count("HeatAttack")))
    print("Number of DrillAttack: "+ str(saved_results.count("DrillAttack")))
    print("Number of FreezerAttack: "+ str(saved_results.count("FreezerAttack")))
    print("Number of OpenLidAttack: "+ str(saved_results.count("OpenLidAttack")))

# Defenses to be executed when Level 1 is reached
def defenseLevel1(return_data):
    if return_data == "Unknown":
        # Unknown attack: ??
        return
    elif return_data == "FreezerAttack":
        # Freeze attack: Overwrite key in RAM
        return
    elif return_data == "HeatAttack":
        # Heat attack: Move data to a safe location
        return
    elif return_data == "DrillAttack":
        # Drill attack: Move data to a safe location
        return
    elif return_data == "OpenLidAttack":
        # Open lid attack: Delete key from RAM
        return


# Defenses to be executed when Level 2 is reached
def defenseLevel2(return_data, saved_sensor_data, xOrder):
    if return_data == "Unknown":
        # Unknown attack: save the data which caused the unknown attack
        now = datetime.now() # current date and time
        csv_filename = str("../data/unknowndata/UnknownAttack"+now.strftime("_%Y_%m_%d__%H-%M-%S")+".csv")
        df = pd.DataFrame(saved_sensor_data)
        if not os.path.isfile(csv_filename):
            df.to_csv(csv_filename, header='column_names')
        else:
            df.to_csv(csv_filename, mode='a', header='column_names')
    elif return_data == "FreezerAttack":
        # Freeze attack: Turn off device
        return
    elif return_data == "HeatAttack":
        # Heat attack: Delete key from RAM
        return
    elif return_data == "DrillAttack":
        # Drill attack: Delete key from RAM
        return
    elif return_data == "OpenLidAttack":
        # Open lid attack: Turn off device
        return
        

# Function to put the pi to sleep
def goToSleep():
    print("Going to sleep")
    return


# This is run first
if __name__ == "__main__":
    # Argument parser to add options and descriptions in when using 'main.py --help'
    parser = argparse.ArgumentParser(description='Deployment script of the energy efficient tamper attack detection and response mechanisms')
    parser.add_argument("-n","--nosensors", action='store_true', help="Use this option when no sensors are connected. Uses previously recorded sensor data as input.")
    args = parser.parse_args()
    # Start the main program with the arguments specified
    main(not args.nosensors)
