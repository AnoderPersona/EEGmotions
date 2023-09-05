import numpy as np
import serial
import time

class Data_reader:
    
    def __init__(self):
        
        self.port               = 'COM3'
        self.batch_size         =   1  # N° of Time windows
        self.freq               =   256 #frequency of EEG-SMT
        self.sec                =   4   #Seconds of data

        self.start_bytes        =  b'\xa5\x5a\x02'
        self.byte_number        =   17  #Number of bytes in signal
        
        self.baud_rate          =   57600
        self.spec_count         =   0
        self.count_max          =   7

        self.downsample128      =   True #If you want the data to be downsample to 128 (only works when freq is 256)
        self.reshapeChannelFirst=   True #If you want the shape of the data to be (batch_size, data, channel) or (batch_size, channel, data)
        self.printingBatchAllowed=  True #If you want to print the batch number in which you are in
        
    def read_data(self):
        
        s = serial.Serial(port=self.port, baudrate=self.baud_rate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None) 
        #Reads data until start bytes found (b'\xa5\x5a\x02')
        res = s.read_until(expected=self.start_bytes)
        
        print('Getting data...')

        full_data = []
        
        for j in range(self.batch_size):

            if (self.printingBatchAllowed): print(f'Batch number {j+1}')

            data = []
            for i in range(self.freq*self.sec):
                        
                res = s.read(self.byte_number)
                res_list = list(res)
                #Process data so it's readable
                data.append(np.array([res_list[1]*self.freq + res_list[2], res_list[3]*self.freq + res_list[4]]))  

            full_data.append(np.array(data))
                
        print('Data done')

        eeg_data = np.array(full_data)

        if (self.downsample128):
            eeg_data = eeg_data[:,::2,:]

        if (self.reshapeChannelFirst):
            eeg_data = np.reshape(eeg_data, (eeg_data.shape[0], eeg_data.shape[2], eeg_data.shape[1])) 

        return eeg_data
