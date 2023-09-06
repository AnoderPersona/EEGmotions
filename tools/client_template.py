import serial
import requests
import read_smt_data
import numpy as np
import json

import turtle

turtle.speed(0)
turtle.hideturtle()

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


def excited():
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

def happy():

    eyes()

    turtle.up()
    turtle.setheading(0)
    turtle.setpos(0,0)

    turtle.goto(-40, -80)
    turtle.down()
    turtle.right(90)
    turtle.circle(40, 180)
    turtle.up()

def sad():

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
            turtle.clear()

            if valence == 0:
                if arousal == 0:
                    # low valence and arousal
                    turtle.Screen().bgcolor("blue")
                    neutral()

                else:
                    # low valence high arousal
                    turtle.Screen().bgcolor("red")
                    sad()

            else:
                if arousal == 0:
                    # high valence low arousal
                    turtle.Screen().bgcolor("yellow")
                    happy()

                else:
                    # high valence and arousal
                    turtle.Screen().bgcolor("orange")
                    excited()

        else:
            print('There was a problem with the transaction')
    
send_data()

