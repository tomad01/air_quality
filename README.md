# air_quality
Read data from various senzors and write to a csv file.\
This script is meant to run on a raspberry pi.\
An Arduino is expected to be serial connected to the raspberry.\
The script works in py2 or 3.

Senzors connected to Raspberry:\
DHT 22 (digital; temperature and humidiy)\
the script assumes the sensor is connected to pin 4\
BMP085 (digital: temperature and pressure)\
the script assumes the sensor is connected to i2c on channel 77 (pin 2 data, 3 clock)\
sudo i2cdetect -y 1" - to check channel


Senzors connected to Arduino UNO:\
MQ-2 Gas (analogic ~ 150 mA)\
Arduino expects the analogic data pin (from sensor) to be connected to pin 0 (analogic from Arduino)\
GP2Y1010AU0F (analogic dust senzor using infrared led - 20 mA, with resistor and capacitor integrated)\
Arduino expects the analogic data pin (from sensor) to be connected to pin 1 (analogic from Arduino) and 
the ledpower digital pin (from senzor) to be conected to pin 2 (digital from Arduino)\
Arduino is waiting from Raspberry an income message and then collects and send data.\
Raspberry gets all data and is writing it down to a csv periodically

The sensors should be powered each as specified in the their datasheets.\
The process is automated using supervisord (see conf files)
You need to create an empty "logs" dir in the script dir before deploying.\
Check requierments files before installing. There are some packages that can be omitted.
