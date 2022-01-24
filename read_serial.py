import serial
import time
import re
serial_regex = re.compile('Value: (\d{1,5}\.\d{1,5}) mill')

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        #if ser.in_waiting > 0:
        #    line = ser.readline().decode('utf-8').rstrip()
        #    print(line)
        ser.write(b"Hello from Raspberry Pi!\n")
        line = ser.readline().decode('utf-8').rstrip()
	result = serial_regex.findall(line)
	if len(result)>0:
	    print(str(result[0]))
        print('waiting')
        time.sleep(5)
