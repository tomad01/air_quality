from datetime import datetime

import time,os,subprocess,sys
import uuid
import logging
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
#os.chdir(dname)
LOG_FILE = 'sensors.log'
logging.basicConfig(filename=dname+'/logs/'+LOG_FILE,
                    format='%(asctime)s %(levelname)s:%(message)s', 
                    level=logging.INFO)
# import argparse
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass
import apihelper.sensors as sens
from apihelper.datawriter import CSVWriter
# from apihelper.email import send_email



# parser = argparse.ArgumentParser()
# parser.add_argument('--debug', type=bool, default=False, help='debug')
# args = parser.parse_args()

SLEEP_TIME = 9
logging.info('py version '+str(sys.version))
process = subprocess.Popen('ifconfig | grep wlan', shell=True, stdout=subprocess.PIPE)
logging.info(process.stdout.read().decode())





session_id = str(uuid.uuid1())
collectors = [sens.CollectDHT22(),sens.CollectBMP180(),sens.CollectArduino(),sens.CollectWIFIdata()]
datawriter = CSVWriter()
# contor = 0
while True:

    # if contor==5:
    #     process = subprocess.Popen('tail -n 7 %s'%datawriter.file_full_path, shell=True, stdout=subprocess.PIPE)
    #     res = process.stdout.read().decode().encode('ascii','ignore')
    #     send_email(res)
    # contor +=1
    
    time.sleep(SLEEP_TIME)    
    collected = [cc.collect() for cc in collectors]
    collected.append({
        'session_id':session_id,
        'timestamp':datetime.strftime(datetime.now(),"%Y-%m-%d %H:%M:%S")
        })
    datawriter.write(collected)           
    if datawriter.file_too_big():
        logging.info('max size limit reached')
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

