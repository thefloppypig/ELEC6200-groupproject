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

    # Init sensors
    bme280, i2c, tsl1, acc = initialiseSensors()

    # Load models
    models01, models11, attackClassificationModel = loadModels()

    # Counters
    i = 0 # Only for instruction count

    # Monitoring storage
    saved_results = []
    saved_sensor_data = []

    # Keep track of defense for future defense/recovery
    defense_triggered = ""
    
    # LOOP ONCE
    while (i == 0):
        i = i + 1

        # Set sampling rate according to risk
        if potential_attacks < no_attacks_1_to_2:
            time.sleep(sr_level_1)
        else:
            time.sleep(sr_level_2)

        # Get models' input data from sensors
        sensor_data = pollSensors(bme280, i2c, tsl1, acc)
        data_entry = []
        for xEntry in xOrder:
            for item in sensor_data:
                if (xEntry == item):
                    data_entry.append(sensor_data.get(item))
        data_entry = np.array(data_entry)

        # Classify data
        return_data, potentials = checkModels(models01, models11, attackClassificationModel, data_entry)
        
        # Store info for monitoring
        saved_results.append(return_data)
        saved_sensor_data.append(sensor_data)

        # Count detected attacks and recover/sleep
        if return_data != "Normal": # If there is an attack
            potential_attacks = potential_attacks + 1
            sleep_count = 0
            reset_count = 0
        elif potential_attacks < no_attacks_1_to_2: # If in level 1 and no attack detected
            sleep_count = sleep_count + 1
            if sleep_count > no_normal_1_to_sleep: # If no attacks when in level 1 for a long time, go to sleep
                goToSleep()
                return
        else: # If in level 2 and no attack detected
            reset_count = reset_count + 1
            potential_attacks = 0
            if reset_count > no_normal_2_to_1: # If no attacks when in level 2 for a long time, reset to level 1
                sleep_count = 0
                recover(defense_triggered)

        # Trigger Defense
        if potential_attacks == no_attacks_1_to_2:
            defenseLevel1(return_data)
            defense_triggered = return_data
        if potential_attacks == no_attacks_2_to_attack:
            defenseLevel2(return_data, saved_sensor_data, xOrder)
            return

# Defenses to be executed when Level 1 is reached
def defenseLevel1(return_data):
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
    if return_data == "Unknown":
        # Unknown attack: save the data which caused the unknown attack
        now = datetime.now() # current date and time
        csv_filename = str(monitor_directory  + "UnknownAttack"+now.strftime("_%Y_%m_%d__%H-%M-%S")+".csv")
        df = pd.DataFrame(saved_sensor_data)
        if not os.path.isfile(csv_filename):
            df.to_csv(csv_filename, header='column_names')
        else:
            df.to_csv(csv_filename, mode='a', header='column_names')
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

# Level 1 to sleep
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
    main()
