#include <avr/sleep.h>
#include <avr/power.h>


const int PIR = 3;     // the number of the pushbutton pin
const int USB_EN =  7;  // the number of the Enable pin
const int RPI_OFF = 6;  // Raspberry Pi power off signal
int PIRval = 0;
int RPI_OFF_val = 0;

void setup()
{
    // Configure wake up pin as input.
    // This will consumes few uA of current.
    pinMode(PIR, INPUT);   
    pinMode(RPI_OFF, INPUT); 
    pinMode(USB_EN, OUTPUT);  
    digitalWrite(USB_EN, LOW); 
    Serial.begin(9600);
      // disable ADC
    ADCSRA = 0;  

      // turn off everything we can
    power_adc_disable ();
    power_spi_disable();
    power_twi_disable();
    power_timer1_disable();
      // turn off brown-out enable in software
    MCUCR = bit (BODS) | bit (BODSE);
    MCUCR = bit (BODS); 
}

void loop() 
{
    delay(200);
    Serial.println("arduino started!");
    PIRval = digitalRead(PIR); 
    RPI_OFF_val = digitalRead(RPI_OFF); 
    if(PIRval == HIGH)
    {
        Serial.println("detected");
        digitalWrite(USB_EN, HIGH);
        int PIRval = 0;
    }
    if(RPI_OFF_val == HIGH)
    {
        Serial.println("shuting off USB switch");
        delay(5000);
        digitalWrite(USB_EN, LOW);
        int RPI_OFF_val = 0;
    }
}
