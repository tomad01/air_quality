
import time
import CWrapper
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN         = 8
samplingTime = 280
deltaTime    = 40
sleepTime    = 9680

print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)



def read_values(ind):
    values = [0]*4
    for i in range(4):  	
        # Read the specified ADC channel using the previously set gain value.
        value = adc.read_adc(i,gain=GAIN) 
        voltage = value * 4/2047.0
        dustDens = 0.17 * voltage  - 1
        values[i] = "%.2f"%dustDens
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    return values[ind]
    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

while True:    
    GPIO.output(18,GPIO.HIGH)
    CWrapper.sleep_usec(samplingTime)
    read_values(3)
    CWrapper.sleep_usec(deltaTime)    
    GPIO.output(18,GPIO.LOW)
    CWrapper.sleep_usec(sleepTime)
            
    time.sleep(0.5)
