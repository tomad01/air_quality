from datetime import datetime
from glob import glob
import time,csv,os,subprocess,re,pdb
import uuid

import pandas as pd
import serial

from Adafruit_BMP import BMP085
import Adafruit_DHT as dht

##########################
PERCENT_FROM_AVAILABLE_SPACE = 0.5 # max space to fill with data
DATA_DIR = './data'
SLEEP_TIME = 9
COLLECT_WIFI_DATA = True
COLLECT_ARDUINO_DATA = True
SERIAL_ADDR = '/dev/ttyACM0'
##########################


def get_dht22_data():
    try:
        h,t = dht.read_retry(dht.DHT22, 4)
    except Exception as er:
        h,t = 0,0
	#print(str(er))	
    return h,t

def get_bmp180_data():
    try:
        # i2c on channel 77 (pin 2 data,pin 3 clock)
        # "sudo i2cdetect -y 1" - to check channel
        bmp = BMP085.BMP085()
        temp = bmp.read_temperature()
        pressure = bmp.read_pressure()
        #altitude = bmp.read_altitude()
    except Exception as er:
	#print(str(er))	
        temp = 0
        pressure = 0
        #altitude = 0
    return temp,pressure

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

file1 = DATA_DIR+'/data_sensors.csv'
add_header = not os.path.exists(file1)
conn1 = open(file1,'a')
writer1 = csv.writer(conn1)
if add_header:
    writer1.writerow(['session_id','timestamp','humidity','temp_dht','pressure','temp_bmp','gas','wifi_conns','90_perc_wifi_power'])
#file2 = DATA_DIR+'/data_wifi.csv'
#conn2 = open(file2,'a')
#writer2 = csv.writer(conn2)

try:
    import psutil,sys
    print('py version',sys.version)
    hdd = psutil.disk_usage('/')
    free = hdd.free/2**30
    limit = int(PERCENT_FROM_AVAILABLE_SPACE *free)
except Exception as er:
    print(str(er))
    limit = 2
print('max GB size allowed of data:',limit)


pattern = re.compile('Signal level=(\-\d{1,2}) dBm\s+\n\s+ESSID:\"(.+?)\"')

ser = serial.Serial(SERIAL_ADDR, 9600, timeout=1)
ser.reset_input_buffer()
serial_regex = re.compile('Value: (\d{1,5}\.\d{1,5}) mill')

# header1
# timestamp,humiddity,temp_dht,pressure,temp_bmp,gas,wifi_conns,90_perc_wifi_power
# header2
# timestamp,power,network
session_id = str(uuid.uuid1())
while True:
    time.sleep(SLEEP_TIME)
    timestamp=datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
    #############################################
    h,t = get_dht22_data()
    temp,pres = get_bmp180_data()
    gas = 0
    if COLLECT_ARDUINO_DATA:
        try:
            ser.write(b"Hello from Raspberry Pi!\n")
            line = ser.readline().decode('utf-8').rstrip()
            gas = str(serial_regex.findall(line)[0])
        except Exception as er:
            gas = 0
            print(str(er))
    else:
        gas = 0

    #############################################
    if COLLECT_WIFI_DATA:
        process = subprocess.Popen('sudo iwlist wlan0 scan | egrep "ESSID|Signal"', shell=True, stdout=subprocess.PIPE)
        res = process.stdout.read().decode()
        ll = []
        for item in pattern.findall(res):
       	    #writer2.writerow([timestamp,item[0],item[1]])
            ll.append(float(item[0]))
        if len(ll)==0:
            ll = [0]        
        power = round(pd.Series(ll).quantile(.9),2)
        #conn2.flush()
    else:
        ll,power = [],0
    #############################################
    writer1.writerow([session_id,timestamp,'%.2f'%h,'%.2f'%t,'%.2f'%pres,'%.2f'%temp,gas,len(ll),power])
    conn1.flush()            
    #############################################
            
    tsize = 0
    for filen in glob(DATA_DIR):
    	tsize += os.path.getsize(filen)
    if tsize/1e6>limit*1000:
        print('max size limit reached')
        break

    
    
"""
//ARDUINO CODE

#define MQ2pin (0)

float sensorValue;  //variable to store sensor value

char message[120];

void setup()
{
  Serial.begin(9600); // sets the serial port to 9600
  //Serial.println("Gas sensor warming up!");
  //delay(20000); // allow the MQ-6 to warm up
}

void loop()
{
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    //Serial.print("You sent me: ");
    //Serial.println(data);
      sensorValue = analogRead(MQ2pin); // read analog input pin 0  
    Serial.print("Sensor Value: ");
    Serial.print(sensorValue);
    Serial.print(" millis: ");
    Serial.print(millis());
    Serial.println("");
  }

  //delay(2000); // wait 2s for next reading
}
"""    

