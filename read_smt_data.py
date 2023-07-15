import numpy as np
import serial
import time

class Data_reader:
    
    def __init__(self):
        
        self.port               = 'COM3'
        self.n                  =   25  # N° of Time windows
        self.time_interval      =   0.2   # Seconds between each time window
        
        self.ch1                = np.zeros(self.n, dtype=int)
        self.ch2                = np.zeros(self.n, dtype=int)
        
        self.start_bytes        =  b'\xa5\x5a\x02'
        
        self.baud_rate          =   57600
        self.spec_count         =   0
        self.count_max          =   7
        
    def read_data(self):
        
        s = serial.Serial(port=self.port, baudrate=self.baud_rate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None) 
        #Reads data until start bytes found (b'\xa5\x5a\x02')
        res = s.read_until(expected=self.start_bytes)
        
        count = 0

        start_time = time.time()
        current_time = start_time
        
        print('Getting data...')
        
        while (count < self.n):
            
            if (current_time - start_time >= self.time_interval):
                
                res = s.read_until(expected=self.start_bytes)
                res_list = list(res)
                
                #Picks ch1_high and ch1_low
                #Processing data so it's usable
                self.ch1[count] = res_list[1]*256 + res_list[2]
                
                self.ch2[count] = res_list[3]*256 + res_list[4]
                
                count += 1
                start_time = time.time()
                
            else:
                current_time = time.time()
                
        print('Data done')

        return [self.ch1.tolist(), self.ch2.tolist()]
