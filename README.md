# air_quality
read data from various senzors

Senzors connected to Raspberry\
DHT 22 (digital; temperature and humidiy)\
BMP085 (digital: temperature and pressure)\

Senzors connected to Arduino UNO:\
MQ-2 Gas (analogic ~ 150 mA)\
GP2Y1010AU0F (analogic dust senzor using infrared led - 20 mA)\

Arduino is waiting from Raspberry an income message and then collects and send data.\
Raspberry gets all data and is writing it down to a csv periodically

The process is automated using supervisord (see conf files)
