from os import listdir, remove, system
from shutil import copy
from random import choice
from string import ascii_letters
from time import sleep
try:
    import RPi.GPIO as GPIO
except:
    print("RPI.GPIO was not imported")

# copy files from one directory to another. Use for moving files to safe location or recovering files from safe location
def copy_files(origin_directory, destination_directory):
    filelist=listdir(origin_directory)

    for item in filelist:
        copy((origin_directory+item),destination_directory)
    

# delete all files in the directory
def delete_files(directory):
    filelist=listdir(directory)
    
    for item in filelist:
        remove((directory+item))

# overwrite the contents of the files in the directory
def overwrite_files(directory):
    filelist=listdir(directory)

    for item in filelist:
        file = open(directory+item,"w")
        file.write(choice(ascii_letters))
        file.close()

# turn off the device
def turn_off_device():
    print("Turning off")
    sleep(1)
    #system('sudo shutdown -h now')
    return

# Create a new key
def new_key(directory):
    filelist=listdir(directory)

    for item in filelist:
        file = open(directory+item,"w")
        file.write("New Key")
        file.close()
        
# Function to put the pi to sleep
def goToSleep():
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(23, GPIO.OUT)# set pin 16 as output
    #GPIO.output(23,GPIO.HIGH)
    print("Going to sleep")
    sleep(1)
    #system('sudo shutdown -h now')
    return