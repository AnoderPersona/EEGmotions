import numpy as np
import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt.QtCore import Qt

import scipy
from scipy import signal

class Plotter:
    def __init__(self):
        #Declaration of variables
        self.n                  =   70
        
        self.ch1 = np.zeros(self.n)
        self.ch2 = np.zeros(self.n)
        
        self.Sxx_acum           =   []
        self.Sxx_acum2          =   []
        
        self.x_lim_eeg_plot     =   (0,70)
        self.y_lim_eeg_plot     =   (-200,1200)
        
        self.x_lim_fftp_plot    =  (0,35)
        self.y_lim_fftp_plot    =  (0,1000)
        
        self.start_bytes        =  b'\xa5\x5a\x02'
        
        self.port               =  'COM3'
        self.baud_rate          =   57600
        self.spec_count         =   0
        self.count_max          =   7
        
        self.x_lim_color_plot    =  (0,self.count_max)
        self.y_lim_color_plot    =  (0,self.count_max)
        
        self.Sxx_acum           =   []
        self.Sxx_acum_2         =   []
            
    def set_port(self, port:str):
        '''Sets the serial port of the reader (has to be 'COM'+number i.e. 'COM3' '''
        self.port = port
        
    def generate_window(self):
        win = pg.GraphicsLayoutWidget(show=True, title="EEG")
        # win.resize(700,700)
        win.setWindowTitle('Real-time signals: Plotting')
        pg.setConfigOptions(antialias=True)
        return win
    
    def generate_plot(self, plot_title:str, x_lim, y_lim):
        plot = self.win.addPlot(title=plot_title)
        plot.setRange(xRange=x_lim, yRange=y_lim)
        curve = plot.plot(pen='y')
        return plot, curve
    
    def generate_colorBarItem(self, plot_title:str):
        img = pg.ImageItem()
        spec1 = self.win.addPlot(title=plot_title)
        spec1.addItem(img, title='' )
        bar = pg.ColorBarItem(
                colorMap='CET-L4',
                label='horizontal color bar',
                orientation = 'v',
                pen='#8888FF', hoverPen='#EEEEFF', hoverBrush='#EEEEFF80',
            )
        return bar, img, spec1
    
    def update(self):
        
        #Reads data until start bytes found (b'\xa5\x5a\x02')
        res = self.s.read_until(expected=self.start_bytes)
        
        #moves data inside channels 1 and 2 so it looks more pleasing
        self.ch1[:-(self.n//3)] = self.ch1[(self.n//3):]
        self.ch2[:-(self.n//3)] = self.ch2[(self.n//3):]

        #updates channel1 and 2's data, but only from positions (2*n)//3 to n-1
        for i in range(2*self.n//3,self.n):
            
            res = self.s.read_until(expected=self.start_bytes)

            res_list = list(res)
            #Picks ch1_high and ch1_low
            #Processing data so it's usable
            self.ch1[i] = res_list[1]*256 + res_list[2]
            
            self.ch2[i] = res_list[3]*256 + res_list[4]

        fft1 =  np.absolute(scipy.fft.rfft(self.ch1-np.mean(self.ch1)))
        fft2 =  np.absolute(scipy.fft.rfft(self.ch2-np.mean(self.ch2)))
                
        #Updating plot data
        self.curve_plot1.setData(self.ch1)
        self.curve_plot2.setData(self.ch2)

        self.curve_fft1.setData(fft1)
        self.curve_fft2.setData(fft2)
        
        Sxx = np.absolute(scipy.fft.rfft(self.ch1))
        Sxx2 = np.absolute(scipy.fft.rfft(self.ch2))

        if (self.spec_count < self.count_max):

            self.Sxx_acum.append(Sxx)

            self.img.setImage(np.array(self.Sxx_acum))
            self.bar.setLevels([min(Sxx), max(Sxx)])
            
            self.Sxx_acum_2.append(Sxx)

            self.img2.setImage(np.array(self.Sxx_acum_2))
            self.bar2.setLevels([min(Sxx2), max(Sxx2)])
            
            self.spec_count += 1

            
        else:            
            self.Sxx_acum.clear()
            self.Sxx_acum_2.clear()

            self.spec_count = 0
            
    def plot(self):
        self.s = serial.Serial(port=self.port, baudrate=self.baud_rate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None) 
        print('Starting...')
        self.spec_count = 0

        
        self.win = self.generate_window()
        
        eeg_plot1, self.curve_plot1 = self.generate_plot('channel 1 in real time: Plotting', self.x_lim_eeg_plot, self.y_lim_eeg_plot)
        eeg_plot2, self.curve_plot2 = self.generate_plot('channel 2 in real time: Plotting', self.x_lim_eeg_plot, self.y_lim_eeg_plot)
        
        self.win.nextRow()
        
        self.fft_plot1, self.curve_fft1 = self.generate_plot('channel 1 fourier in real time: Plotting', self.x_lim_fftp_plot, self.y_lim_fftp_plot)
        self.fft_plot2, self.curve_fft2 = self.generate_plot('channel 2 fourier in real time: Plotting', self.x_lim_fftp_plot, self.y_lim_fftp_plot)
        
        self.win.nextRow()
        
        self.bar, self.img, self.color_plot= self.generate_colorBarItem("Spectogram ch1")
        self.bar2, self.img2, self.color_plot2 = self.generate_colorBarItem("Spectogram ch2")
        
        self.color_plot.addLine(y=3, pen=pg.mkPen('r', width=1))
        self.color_plot.addLine(y=7, pen=pg.mkPen('r', width=1))
        self.color_plot.addLine(y=13, pen=pg.mkPen('r', width=1))
        self.color_plot.addLine(y=30, pen=pg.mkPen('r', width=1))
        self.color_plot.addLine(y=50, pen=pg.mkPen('r', width=1))
        
        self.color_plot2.addLine(y=3, pen=pg.mkPen('r', width=1))
        self.color_plot2.addLine(y=7, pen=pg.mkPen('r', width=1))
        self.color_plot2.addLine(y=13, pen=pg.mkPen('r', width=1))
        self.color_plot2.addLine(y=30, pen=pg.mkPen('r', width=1))
        self.color_plot2.addLine(y=50, pen=pg.mkPen('r', width=1))

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)

        #Milliseconds interval between data updates
        timer.start(150)
        pg.exec()

