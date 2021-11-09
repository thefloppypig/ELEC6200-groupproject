import os
import shutil
import time
import RPi.GPIO as GPIO

def main():
    while True:
        response('normal')
        time.sleep(3)
        response('normal')
        time.sleep(3)
        response('normal')
        time.sleep(3)
        response('normal')
        time.sleep(3)
        response('openlid')

def response(threat): #function to activate copy/delete/recover file
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT)# set pin 16 as output
    if threat=='freeze'or threat=='openlid': #in case of freeze /open lid attack
        delete_files()
        GPIO.output(23,GPIO.HIGH)
        time.sleep(1)
        os.system('sudo shutdown -h now')
    elif threat=='drill' or threat=='heater':#in case of drill /heat attack

        copy_files_to_safe_location()
        delete_files()
        GPIO.output(23,GPIO.HIGH)
        time.sleep(1)
        os.system('sudo shutdown -h now')

def copy_files_to_safe_location():
    filelist=os.listdir('/media/pi/LH TOSHIBA/dummy/datafile')
    #print(filelist)

    for item in filelist:
        shutil.copy(('/media/pi/LH TOSHIBA/dummy/datafile/'+item),'/media/pi/LH TOSHIBA/dummy/recovery')    
    
    #print(os.listdir('/media/pi/LH TOSHIBA/dummy/recovery'))
    
def delete_files():
    filelist=os.listdir('/media/pi/LH TOSHIBA/dummy/datafile')
    
    for item in filelist:
        os.remove(('/media/pi/LH TOSHIBA/dummy/datafile/'+item))
    
def copy_files_from_safe_location():
    filelist=os.listdir('/media/pi/LH TOSHIBA/dummy/datafile')
    
    for item in filelist:
        shutil.copy(('/media/pi/LH TOSHIBA/dummy/recovery/'+item),'/media/pi/LH TOSHIBA/dummy/datafile')
    
if __name__ == "__main__":
    main()    