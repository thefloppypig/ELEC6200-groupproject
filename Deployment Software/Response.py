import os
import shutil
import random
import string

# copy files from one directory to another. Use for moving files to safe location or recovering files from safe location
def copy_files(origin_directory, destination_directory):
    filelist=os.listdir(origin_directory)

    for item in filelist:
        shutil.copy((origin_directory+item),destination_directory)    
    

# delete all files in the directory
def delete_files(directory):
    filelist=os.listdir(directory)
    
    for item in filelist:
        os.remove((directory+item))

# overwrite the contents of the files in the directory
def overwrite_files(directory):
    filelist=os.listdir(directory)

    for item in filelist:
        file = open(directory+item,"w")
        file.write(random.choice(string.ascii_letters, 5))
        file.close()

# turn off the device
def turn_off_device():
    os.system('sudo shutdown -h now')

# Create a new key
def new_key(directory):
    filelist=os.listdir(directory)

    for item in filelist:
        file = open(directory+item,"w")
        file.write("New Key")
        file.close()