import serial
import requests
import read_smt_data
import numpy as np
import json

import turtle

turtle.speed(0)

def send_data():

    server_url = 'http://localhost:8000'


    for i in range(100):
        reader = read_smt_data.Data_reader()
        eeg_data = reader.read_data().tolist()

        print('Sending data')
        res = requests.post(f'{server_url}/data/raw/',
            headers = {
                'Content-type': 'application/json'
            },
            json = {"data": str(eeg_data)},
        )
        if (res.status_code == 200):
            print(res.json())
            valence = res.json()[0]
            arousal = res.json()[1]

            if valence == 0:
                if arousal == 0:
                    # low valence and arousal
                    turtle.Screen().bgcolor("blue")

                else:
                    # low valence high arousal
                    turtle.Screen().bgcolor("red")

            else:
                if arousal == 0:
                    # high valence low arousal
                    turtle.Screen().bgcolor("light blue")

                else:
                    # high valence and arousal
                    turtle.Screen().bgcolor("yellow")



        else:
            print('There was a problem with the transaction')
    
send_data()

