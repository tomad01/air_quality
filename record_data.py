from datetime import datetime
from glob import glob
import time,csv,os,subprocess,re,pdb,sys
import uuid

import pandas as pd
import serial

from Adafruit_BMP import BMP085
import Adafruit_DHT as dht

print('py version',sys.version)
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

file1 = DATA_DIR+'/data_sensors2.csv'
add_header = not os.path.exists(file1)
conn1 = open(file1,'a')
writer1 = csv.writer(conn1)
if add_header:
    writer1.writerow(['session_id','timestamp','humidity','temp_dht','pressure','temp_bmp','wifi_conns','90_perc_wifi_power','dust','gas'])
#file2 = DATA_DIR+'/data_wifi.csv'
#conn2 = open(file2,'a')
#writer2 = csv.writer(conn2)

try:
    import psutil
    hdd = psutil.disk_usage('/')
    free = hdd.free/2**30
    limit = int(PERCENT_FROM_AVAILABLE_SPACE *free)
except Exception as er:
    print(str(er))
    limit = 2
print('max GB size allowed of data:',limit)


wifi_regex = re.compile('Signal level=(\-\d{1,2}) dBm\s+\n\s+ESSID:\"(.+?)\"')

ser = serial.Serial(SERIAL_ADDR, 9600, timeout=1)
ser.reset_input_buffer()
serial_regex = re.compile('ust: (\d+\.\d+) ug\/m3 gas: (\d+\.\d+) en')


session_id = str(uuid.uuid1())
while True:
    time.sleep(SLEEP_TIME)
    timestamp=datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
    #############################################
    h,t = get_dht22_data()
    temp,pres = get_bmp180_data()
    gas,dust = 0,0
    if COLLECT_ARDUINO_DATA:
        try:
            ser.write(b"Hello from Raspberry Pi!\n")
            line = ser.readline().decode('utf-8').rstrip()
	    line = serial_regex.findall(line)
            gas  = float(str(line[0][1].encode('ascii','ignore')))
            dust = float(str(line[0][0].encode('ascii','ignore')))
        except Exception as er:

            print(str(er))
    #############################################
    if COLLECT_WIFI_DATA:
        process = subprocess.Popen('sudo iwlist wlan0 scan | egrep "ESSID|Signal"', shell=True, stdout=subprocess.PIPE)
        res = process.stdout.read().decode()
        ll = []
        for item in wifi_regex.findall(res):
       	    #writer2.writerow([timestamp,item[0],item[1]])
            ll.append(float(item[0]))
        if len(ll)==0:
            ll = [0]        
        power = round(pd.Series(ll).quantile(.9),2)
        #conn2.flush()
    else:
        ll,power = [],0
    #############################################
    writer1.writerow([session_id,timestamp,'%.2f'%h,'%.2f'%t,'%.2f'%pres,'%.2f'%temp,len(ll),power,dust,gas])
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

int measurePin = 1; //Connect dust sensor to Arduino A0 pin
int gasPin = 0; //MQ -2 senzor
int ledPower = 2;   //Connect led driver pins of dust sensor to Arduino D2
int samplingTime = 280;
int deltaTime = 40;
int sleepTime = 9680;
float voMeasured = 0;
float gasMeasured = 0;

float calcVoltage = 0;
float dustDensity = 0;
void setup(){
  Serial.begin(9600);
  pinMode(ledPower,OUTPUT);
  Serial.print("****************** keyestudio ******************\n");
}
void loop(){
if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    digitalWrite(ledPower,LOW); // power on the LED
    delayMicroseconds(samplingTime);
    voMeasured = analogRead(measurePin); // read the dust value
    gasMeasured = analogRead(gasPin); // read the MQ value
    delayMicroseconds(deltaTime);
    digitalWrite(ledPower,HIGH); // turn the LED off
    delayMicroseconds(sleepTime);
    // 0 - 5V mapped to 0 - 1023 integer values
    // recover voltage
    calcVoltage = voMeasured * (5.0 / 1024.0);
    dustDensity = 170 * calcVoltage - 0.1;
    Serial.print("dust: ");
    Serial.print(dustDensity);
    Serial.print(" ug/m3 ");  
    Serial.print("gas: ");
    Serial.print(gasMeasured);
    Serial.print(" end \n");       
    }   
}
//******************************************************************
"""    

