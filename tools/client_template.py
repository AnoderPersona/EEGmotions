import serial
import requests
import read_smt_data
import numpy as np
import json

import turtle

#turtle config
turtle.speed(0)
turtle.hideturtle()
turtle.width(4)

# Face drawing functions
# PLEASE KEEP IN MIND THAT THE NAMES ARE JUST REFERENTIAL
def eyes():
    turtle.up()
    turtle.goto(-80, -50)
    turtle.setheading(0)
    eye()
    turtle.goto(80, -50)
    turtle.setheading(0)
    eye()

def eye():

    turtle.down()
    turtle.fillcolor('white')
    turtle.begin_fill()
    turtle.circle(50)
    turtle.end_fill()
    turtle.up()


def high_valence_high_arousal():
    eyes()

    turtle.up()
    turtle.setheading(0)
    turtle.setpos(0,0)

    turtle.goto(-40, -80)
    turtle.down()
    turtle.goto(40, -80)
    turtle.up()

    turtle.goto(-40, -80)
    turtle.down()
    turtle.right(90)
    turtle.circle(40, 180)
    turtle.up()

def high_valence_low_arousal():

    eyes()

    turtle.up()
    turtle.setheading(0)
    turtle.setpos(0,0)

    turtle.goto(-40, -80)
    turtle.down()
    turtle.right(90)
    turtle.circle(40, 180)
    turtle.up()

def low_valence_high_arousal():

    eyes()

    turtle.up()
    turtle.setheading(0)
    turtle.setpos(0,0)

    turtle.goto(-40, -80)
    turtle.down()
    turtle.goto(40, -80)
    turtle.up()

    turtle.goto(40, -80)
    turtle.down()
    turtle.left(90)
    turtle.circle(40, 180)
    turtle.up()

def low_valence_low_arousal():

    eyes()

    turtle.up()
    turtle.setheading(0)
    turtle.setpos(0,0)

    turtle.goto(40, -80)
    turtle.down()
    turtle.left(90)
    turtle.circle(40, 180)
    turtle.up()

def neutral():

    eyes()

    turtle.up()
    turtle.setheading(0)
    turtle.setpos(0,0)

    turtle.goto(-40, -80)
    turtle.down()
    turtle.goto(40, -80)
    turtle.up()

# Funtion that connects to API-----------------------------------------------------
def send_data():

    server_url = 'http://localhost:8000'

    for i in range(100):

        # Reads sends data to API
        reader = read_smt_data.Data_reader()
        eeg_data = reader.read_data().tolist()

        print('Sending data')
        res = requests.post(f'{server_url}/data/raw/',
            headers = {
                'Content-type': 'application/json'
            },
            json = {"data": str(eeg_data)},
        )

        # If the API response is succesful, background color and face changes
        if (res.status_code == 200):
            print(res.json())
            valence = res.json()[0]
            arousal = res.json()[1]
            turtle.clear()

            if valence == 0:
                if arousal == 0:
                    # low valence and arousal
                    turtle.Screen().bgcolor("blue")
                    low_valence_low_arousal()

                else:
                    # low valence high arousal
                    turtle.Screen().bgcolor("red")
                    low_valence_high_arousal()

            elif valence == 1:
                if arousal == 0:
                    # high valence low arousal
                    turtle.Screen().bgcolor("yellow")
                    high_valence_low_arousal()

                else:
                    # high valence and arousal
                    turtle.Screen().bgcolor("orange")
                    high_valence_high_arousal()

            else:
                # neutral within neutral threshold
                turtle.Screen().bgcolor("gray")
                neutral()


        else:
            print('There was a problem with the transaction')
    
send_data()

