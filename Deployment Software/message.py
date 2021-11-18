# function to send sms when attack detected

import serial, time

def main():
    sendmsg()

# takes attack name and sender number to alert owner of number of any attacks
def sendmsg(attack='no response', receiver='+447591576004'):
    with serial.Serial('/dev/serial0', 9600, timeout=1) as ser:
        ser.write(b"AT\r\n")
        line = ser.readlines() # reads line to check if sim800l is working properly
        print (line)
        cmd='AT+CMGF=1\r'
        ser.write(cmd.encode())
        time.sleep(0.1)
        cmd1='AT+CMGS='
        cmd2='"'+receiver+'"'+'\r' # sets which number it sends message to"
        cmd=cmd1+cmd2
        ser.write(cmd.encode())
        time.sleep(0.1)
        msg = "Device detected with"+attack+ "attack" # the message sent
        ser.write (msg.encode())
        ser.write (chr(26).encode())
        line2 = ser.readlines() # reading response from the sim800l module if the message is sent successfully
        print (line2)
        ser.close
        
if __name__ == "__main__":
    main()
