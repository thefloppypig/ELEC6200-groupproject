import os
import shutil
import time
import RPi.GPIO as GPIO

def main():
    #copyfile()
    return


def response(threat): #function to activate copy/delete/recover file
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT)# set pin 16 as output
    if threat=='freeze'or threat=='openlid': #in case of freeze /open lid attack
        deletefile()
        GPIO.output(23,GPIO.HIGH) # sents high signal to other controller
        time.sleep(1)
        os.system('sudo shutdown -h now') # shutsdown RPi after 1 second
        
    elif threat=='drill' or threat=='heater':#in case of drill /heat attack
        copyfile()
        deletefile()
        GPIO.output(23,GPIO.HIGH)
        time.sleep(1)
        os.system('sudo shutdown -h now')

def copyfile():
    filelist=os.listdir('/media/pi/LH TOSHIBA/dummy/datafile') # find files in data file and copy names
    #print(filelist)

    for item in filelist: 
        shutil.copy(('/media/pi/LH TOSHIBA/dummy/datafile/'+item),'/media/pi/LH TOSHIBA/dummy/recovery')    
        # copy files into recovery folder
    
    #print(os.listdir('/media/pi/LH TOSHIBA/dummy/recovery'))
    
def deletefile():
    filelist=os.listdir('/media/pi/LH TOSHIBA/dummy/datafile') # find files in directory and copy names
    
    for item in filelist:
        os.remove(('/media/pi/LH TOSHIBA/dummy/datafile/'+item)) # delete files in folder
    
def recoverfile():
    filelist=os.listdir('/media/pi/LH TOSHIBA/dummy/datafile')# find files in recovery file and copy names
    
    for item in filelist:
        shutil.copy(('/media/pi/LH TOSHIBA/dummy/recovery/'+item),'/media/pi/LH TOSHIBA/dummy/datafile')
        # copy files back into data folder
    
if __name__ == "__main__":
    main()    
