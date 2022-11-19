
import Adafruit_DHT as dht
from Adafruit_BMP import BMP085
import logging
import re,serial,subprocess
from apihelper.email import send_email

def create_row(collected,header):
    res = {}
    for di in collected:
        res.update(di)
    return [res[item] for item in header]

class CollectDHT22:
    def __init__(self):
        pass
    def collect(self):
        try:
            h,t = dht.read_retry(dht.DHT22, 4)
        except Exception as er:
            h,t = 0,0
        #print(str(er))	
        return {'humidity':'%.2f'%h,'temp_dht':'%.2f'%t}

class CollectBMP180:
    def __init__(self):
        pass
    def collect(self):
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

        return {'pressure':'%.2f'%pressure,'temp_bmp':'%.2f'%temp}




class CollectArduino:
    def __init__(self):
        SERIAL_ADDR = '/dev/ttyACM0'
        try:
            self.ser = serial.Serial(SERIAL_ADDR, 9600, timeout=1)
            self.ser.reset_input_buffer()
        except Exception as er:
            logging.error(str(er))
        self.serial_regex = re.compile('ust: (\d+\.\d+) ug\/m3 gas: (\d+\.\d+) en')
    def collect(self):
    
        try:
            self.ser.write(b"Hello from Raspberry Pi!\n")
            line = self.ser.readline().decode('utf-8').rstrip()
            line = self.serial_regex.findall(line)
            gas  = float(str(line[0][1].encode('ascii','ignore')))
            dust = float(str(line[0][0].encode('ascii','ignore')))
            if gas>100:
                send_email('warning gas over 100 %f'%gas)
        except Exception as er:
            gas,dust =0,0
            #logging.error(str(er))
        return {'dust':dust,'gas':gas}


class CollectWIFIdata:
    def __init__(self):
        self.wifi_regex = re.compile('Signal level=(\-\d{1,2}) dBm\s+\n\s+ESSID:\"(.+?)\"')

    def collect(self):
        try:
            process = subprocess.Popen('sudo iwlist wlan0 scan | egrep "ESSID|Signal"', shell=True, stdout=subprocess.PIPE)
            res = process.stdout.read().decode()
            ll = []
            for item in self.wifi_regex.findall(res):
                #writer2.writerow([timestamp,item[0],item[1]])
                ll.append(float(item[0]))
            if len(ll)==0:
                ll = [0]      
            fll = [i for i in ll if i > - 90]  
            power = round(sum(fll)/len(fll),2)
            #conn2.flush()
        except:
            ll,power = [],0
        return {'wifi_conns':len(ll),'mean_wifi_power':power}