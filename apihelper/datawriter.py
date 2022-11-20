import csv,os,logging
# from abc import ABC, abstractmethod
from glob import glob

class DATASaver(object):
    def __init__(self):
        self.DATA_DIR = './data'
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)        
        PERCENT_FROM_AVAILABLE_SPACE = 0.5 # max space to fill with data
        try:
            import psutil
            hdd = psutil.disk_usage('/')
            free = hdd.free/2**30
            self.LIMIT = int(PERCENT_FROM_AVAILABLE_SPACE *free)
        except Exception as er:
            logging.error(str(er))
            self.LIMIT = 2
        logging.info('max GB size allowed of data: '+str(self.LIMIT))
        self._contor = 0

    #@abstractmethod        
    def write(self):
        pass

    def file_too_big(self):
        self._contor += 1
        if self._contor==3:
            tsize = sum([os.path.getsize(filen) for filen in glob(self.DATA_DIR)])
            self._contor = 0
            return tsize/1e6>self.LIMIT*1000
        else:
            return False

def create_row(collected,header):
    res = {}
    for di in collected:
        res.update(di)
    return [res[item] for item in header]



class CSVWriter(DATASaver):
    def __init__(self):
        super(CSVWriter,self).__init__()
        DATA_FILE_NAME = 'data_sensors.csv'
        file1 = self.DATA_DIR+'/'+DATA_FILE_NAME
        write_header = not os.path.exists(file1)
        self.conn1 = open(file1,'a')
        self.writer1 = csv.writer(self.conn1)
        self.header = ['session_id','timestamp','humidity','temp_dht','pressure','temp_bmp','wifi_conns','mean_wifi_power','dust','gas']
        if write_header:
            self.writer1.writerow(self.header)
    def write(self,data):        
        self.writer1.writerow(create_row(data,self.header))
        self.conn1.flush() 