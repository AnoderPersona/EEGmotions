# EEGmotions (WIP)

EEGmotions is an API based on fastAPI, capable of reading signals of an EEG-SMT reader. The API processes the signals from the two channels through an AI model, resulting in labels that describe real-time emotions through valence and arousal. With the help of EEGmotions, it will be easier to develop software that responds to emotions from EEG signals.

## Tools

To visualize the signals being read, the tool 'debug_plotter' shows six graphs showing the data. These consists of the raw EEG data, the fft, and the spectogram of both channels. By default the plotter reads through the COM3 port.
Using pyQTGraph, it allows the graphs to be interactive, so if you right click on any of them, it will give you the default options to try.

## The model

The model used for EEGmotions is a CNN from the repository [Emotion-Recognition-from-brain-EEG-signals](https://github.com/siddhi5386/Emotion-Recognition-from-brain-EEG-signals-). Using DEAP dataset to train both arousal and valence into two different classes (positive-negative), this version of the model predicts both by using only two channels; FP2 and F8 in that order.

Both models ended up with about 0,69 - 0,70 of accuracy for arousal and valence respectevely for the dataset. This version of the model is mostly used for demonstration, *I highly suggest to use your own model if you want to get the best results.*

## client_template.py

This project includes a test client for the API. This client gets the data of the EEG-SMT using the read_smt_data.py tool, and then sends it to EEGmotions API. After the prediction, it receives the data back, and shows the state with 5 different cases.
