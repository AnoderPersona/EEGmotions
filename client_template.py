import serial
import requests
import read_smt_data
import numpy as np

def send_data():

    server_url = 'http://localhost:8000'
    reader = read_smt_data.Data_reader()
    eeg_data = reader.read_data()

    print('Sending data')
    res = requests.post(f'{server_url}/data/raw/',
        headers = {
            #'User-agent'  : 'Internet Explorer/2.0',
            'Content-type': 'application/json'
        },
        json = {"data": str(eeg_data)},
    )
    print(res)
    
send_data()
