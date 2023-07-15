# EEGmotions (WIP)

 *This project is still being worked on* 

EEGmotions will be an API based on fastAPI, capable of reading signals of an EEG-SMT reader. The API will process the signals from the two channels through an AI model, resulting in labels that describe real-time emotions. With the help of EEGmotions, it will be easier to develop software that responds to emotions from EEG signals.

## Tools

To visualize the signals being read, the tool 'debug_plotter' shows six graphs showing the data. These consists of the raw EEG data, the fft, and the spectogram of both channels. By default the plotter reads through the COM3 port.

Using pyQTGraph, it allows the graphs to be interactive, so if you right click on any of them, it will give you the default options to try.
