from datetime import datetime
from glob import glob
import time,csv,os,subprocess,sys
import uuid
import logging
import argparse
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass
# from apihelper.email import send_email
import apihelper.sensors as sens
##########################
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
##########################
parser = argparse.ArgumentParser()
parser.add_argument('--debug', type=bool, default=False, help='debug')
args = parser.parse_args()
##########################
PERCENT_FROM_AVAILABLE_SPACE = 0.5 # max space to fill with data
DATA_DIR = './data'
SLEEP_TIME = 9
DATA_FILE_NAME = 'data_sensors_test.csv' if args.debug else 'data_sensors.csv'
LOG_FILE = 'sensors_test.log' if args.debug else 'sensors.log'
DEBUG = args.debug
##########################
logging.basicConfig(filename=dname+'/logs/'+LOG_FILE,
                    format='%(asctime)s %(levelname)s:%(message)s', 
                    level=logging.INFO)
logging.info('py version '+str(sys.version))
process = subprocess.Popen('ifconfig | grep wlan', shell=True, stdout=subprocess.PIPE)
logging.info(process.stdout.read().decode())


if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

file1 = DATA_DIR+'/'+DATA_FILE_NAME
write_header = not os.path.exists(file1)
conn1 = open(file1,'a')
writer1 = csv.writer(conn1)
header = ['session_id','timestamp','humidity','temp_dht','pressure','temp_bmp','wifi_conns','mean_wifi_power','dust','gas']
if write_header:
    writer1.writerow(header)
#file2 = DATA_DIR+'/data_wifi.csv'
#conn2 = open(file2,'a')
#writer2 = csv.writer(conn2)

try:
    import psutil
    hdd = psutil.disk_usage('/')
    free = hdd.free/2**30
    limit = int(PERCENT_FROM_AVAILABLE_SPACE *free)
except Exception as er:
    logging.error(str(er))
    limit = 2
logging.info('max GB size allowed of data: '+str(limit))


session_id = str(uuid.uuid1())
# contor = 0
collectors = [sens.CollectDHT22(),sens.CollectBMP180(),sens.CollectArduino(),sens.CollectWIFIdata()]
while True:
    # if contor==5:
    #     process = subprocess.Popen('tail -n 7 %s'%file1, shell=True, stdout=subprocess.PIPE)
    #     res = process.stdout.read().decode().encode('ascii','ignore')
    #     send_email(res)
    #############################################    
    time.sleep(SLEEP_TIME)    
    collected = [cc.collect() for cc in collectors]
    collected.append({'session_id':session_id,'timestamp':datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")})
    writer1.writerow(sens.create_row(collected,header))
    conn1.flush()            
    #############################################                
    tsize = sum([os.path.getsize(filen) for filen in glob(DATA_DIR)])
    if tsize/1e6>limit*1000:
        logging.info('max size limit reached')
        break
    # contor +=1
    
    
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

