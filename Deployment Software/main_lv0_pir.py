############# This is edited version from main.py (download/project/deployment_software/main.py file)
from time import time, sleep
from numpy.core.numeric import Infinity, array
from pandas import DataFrame
from config import *
from datetime import datetime
from argparse import ArgumentParser
from os.path import isfile
from math import ceil

from LoadModels import loadModels
from Sensors import initialiseSensors, pollSensors
from FakeSensors import loadFakeSensorData, pollFakeSensors
from Response import *

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
    sleep(3)
    print("program started")
    
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
    if (not sensors_connected): 
        bme280, i2c, tsl1, acc = None, None, None, None
        sensor_data_from_files, lines = loadFakeSensorData(attack, use_realdata)
    else: 
        bme280, i2c, tsl1, acc = initialiseSensors()
        sensor_data_from_files, lines = None, Infinity 

    #Load models
    models01, models11, attackClassificationModel = loadModels()

    #Counters
    round = 0
    sleep_count = 0
    current_line = 0
    true_positive = 0
    potential_attacks = 0
    sleep_mode = True

    #Monitoring data (Unknown attacks)
    saved_results = []
    saved_sensor_data = []
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN) # set pin 16 as input
    
    defense_triggered = ""
    while (1):
        sleep_mode = defenseLevel0(sleep_mode)
        while (sleep_mode == False):#current_line < lines): <--- edited
            # Monitoring sensors begins
            if potential_attacks < no_attacks_1_to_2:
                sleep(ceil(sr_level_1))
                sampling_rate = sr_level_1
            else:
                sleep(ceil(sr_level_2))
                sampling_rate = sr_level_2
            # print("-------------------------")
            start_time_all = time()
    
            # Get data from the sensors
            sensor_data = pollSensors(bme280, i2c, tsl1, acc) if sensors_connected else pollFakeSensors(sensor_data_from_files, current_line)
            current_line = current_line + sampling_rate
            # print("Input: " +str(sensor_data)) #################### to be uncomment
            # Format Data to be sent into the models
            data_entry = []
            for xEntry in xOrder:
                for item in sensor_data:
                    if (xEntry == item):
                        data_entry.append(sensor_data.get(item))
    
            data_entry = array(data_entry)
    
            # Send Data to the models for classification
            start_time_ml = time()
            return_data, potentials = checkModels(models01, models11, attackClassificationModel, data_entry)
            end_time_ml = time()
            round = round + 1
            saved_results.append(return_data)
            saved_sensor_data.append(sensor_data)
    
            # Count detected attacks
            if return_data != "Normal": # If there is an attack
                if(potential_attacks > no_attacks_2_to_attack): #<--- edited
                    potential_attacks = 0
                potential_attacks = potential_attacks + 1
                sleep_count = 0
                reset_count = 0
            elif not (potential_attacks < no_attacks_1_to_2): # If in level 2 and no attack detected
                reset_count = reset_count + 1
                potential_attacks = 0
                if reset_count > no_normal_2_to_1: # No attacks when in level 2 for a long time, reset to level 1
                    sleep_count = 0
                    recover(defense_triggered)
            elif potential_attacks < no_attacks_1_to_2: # If in level 1 and no attack detected
                sleep_count = sleep_count + 1
                if sleep_count > no_normal_1_to_sleep:
                    sleep_mode = True
                    goToSleep()
                    #return  <--- edited

            # Output 
            if (str(return_data) == attack):
                true_positive = true_positive + 1
            
            end_time_all = time()
            print("Output: "+ return_data + " | Expected: " + attack + " | Model Time: " + str(end_time_ml-start_time_ml) + " | Total Time: " + str(end_time_all-start_time_all))
    
    
            # Trigger Defense
            if potential_attacks == no_attacks_1_to_2:
                defenseLevel1(return_data)
                defense_triggered = return_data
            if potential_attacks == no_attacks_2_to_attack:
                defenseLevel2(return_data, saved_sensor_data, xOrder)
                sleep_mode = True
                # return <--- edited
            # Summary of output after while loop completes
        #print("Accuracy: "+str(true_positive/round) + " | " + str(true_positive) + "/" + str(round)) <--- edited
        #print("Number of Normal: "+ str(saved_results.count("Normal")))          
        #print("Number of Unknowns: "+ str(saved_results.count("Unknown")))
        #print("Number of HeatAttack: "+ str(saved_results.count("HeatAttack")))
        #print("Number of DrillAttack: "+ str(saved_results.count("DrillAttack")))
        #print("Number of FreezerAttack: "+ str(saved_results.count("FreezerAttack")))
        #print("Number of OpenLidAttack: "+ str(saved_results.count("OpenLidAttack")))

# Defenses to be executed when Level 0 at the start
def defenseLevel0(sleep_mode):       #<--- edited
    print("Defense Level 0 is activated")
    while(1):
        if (GPIO.input(23)==1):
            print("Motion detected!")
            sleep_mode = False
            return sleep_mode
        sleep(0.5)
        #print("PIR scanning")
    
# Defenses to be executed when Level 1 is reached
def defenseLevel1(return_data):
    print("Defense Level 1 is activated")
    if return_data == "Unknown":
        # Unknown attack: ??
        return 
    elif return_data == "FreezerAttack":
        # Freeze attack: Delete key in RAM
        overwrite_files(RAM_directory)
        return
    elif return_data == "HeatAttack":
        # Heat attack: Move data to a safe location
        copy_files(RAM_directory, safe_directory)
        return
    elif return_data == "DrillAttack":
        # Drill attack: Move data to a safe location
        copy_files(RAM_directory, safe_directory)
        return
    elif return_data == "OpenLidAttack":
        # Open lid attack: Delete key from RAM
        overwrite_files(RAM_directory)
        return


# Defenses to be executed when Level 2 is reached
def defenseLevel2(return_data, saved_sensor_data, xOrder):
    print("Defense Level 2 is activated")
    if return_data == "Unknown":
        # Unknown attack: save the data which caused the unknown attack
        now = datetime.now() # current date and time
        csv_filename = str(monitor_directory  + "UnknownAttack"+now.strftime("_%Y_%m_%d__%H-%M-%S")+".csv")
        df = DataFrame(saved_sensor_data)
        if not isfile(csv_filename):
            df.to_csv(csv_filename, header='column_names')
        else:
            df.to_csv(csv_filename, mode='a', header='column_names')
        return # <--- edited
    elif return_data == "FreezerAttack":
        # Freeze attack: Turn off device
        turn_off_device()
        return
    elif return_data == "HeatAttack":
        # Heat attack: Delete key from RAM
        delete_files(RAM_directory)
        turn_off_device()
        return
    elif return_data == "DrillAttack":
        # Drill attack: Delete key from RAM
        delete_files(RAM_directory)
        turn_off_device()
        return
    elif return_data == "OpenLidAttack":
        # Open lid attack: Turn off device
        turn_off_device()
        return
        

def recover(defense_triggered):
    if defense_triggered == "Unknown":
        # Unknown attack: ??
        return 
    elif defense_triggered == "FreezerAttack":
        # Freeze attack: Generate a new key since it was deleted
        new_key(RAM_directory)
        return
    elif defense_triggered == "HeatAttack":
        # Heat attack: Remove data that was moved to a safe location, it is still stored in RAM
        delete_files(safe_directory)
        return
    elif defense_triggered == "DrillAttack":
        # Drill attack: Remove data that was moved to a safe location, it is still stored in RAM
        delete_files(safe_directory)
        return
    elif defense_triggered == "OpenLidAttack":
        # Open lid attack: Generate a new key since it was deleted
        new_key(RAM_directory)
        return   


# This is run first
if __name__ == "__main__":
    # Argument parser to add options and descriptions in when using 'main.py --help'
    parser = ArgumentParser(description='Deployment script of the energy efficient tamper attack detection and response mechanisms')
    parser.add_argument("-n","--nosensors", action='store_true', help="Use this option when no sensors are connected. Uses previously recorded sensor data as input.")
    args = parser.parse_args()
    # Start the main program with the arguments specified
    main(not args.nosensors)