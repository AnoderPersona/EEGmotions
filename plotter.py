import numpy as np
import serial
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import scipy
import random
    
#--------------------------------------------------------------------------------------

def generate_plot(plot_title:str, x_range:list, y_range: list, win):
    plot = win.addPlot(title=plot_title)
    plot.setRange(xRange=x_range, yRange=y_range)
    curve = plot.plot(pen='y')
    return plot, curve

#--------------------------------------------------------------------------------------

def generate_colorBarItem(plot_title:str, win):
    img = pg.ImageItem()
    spec1 = win.addPlot(title=plot_title)
    spec1.addItem(img, title='' )
    bar = pg.ColorBarItem(
            colorMap='CET-L4',
            label='horizontal color bar',
            orientation = 'v',
            pen='#8888FF', hoverPen='#EEEEFF', hoverBrush='#EEEEFF80'
        )
    return bar, img

#--------------------------------------------------------------------------------------

#Setear la win
def generate_window():
    app = pg.mkQApp("Real-time signals")
    win = pg.GraphicsLayoutWidget(show=True, title="EEG")
    win.resize(1000,600)
    win.setWindowTitle('Real-time signals: Plotting')
    pg.setConfigOptions(antialias=True)

    return win

#--------------------------------------------------------------------------------------


#Function that updates all the plots data in real time
def update(s, start_bytes, n, ch1, ch2, fft1, fft2, curve, curve2, curve3, curve4, img, bar, img2, bar2):
    
    # global ch1, ch2, n

    #Leer hasta encontrar los bytes esperados (b'\xa5\x5a\x02')
    res = s.read_until(expected=start_bytes)

    #Lee n arreglos de bytes
    for i in range(n):
        
        res = s.read_until(expected=start_bytes)

        res_list = list(res)
        #Se elige canal ch1_high y ch1_low
        #Se procesa para que sea legible
        ch1[i] = res_list[1]*256 + res_list[2]
        ch2[i] = res_list[3]*256 + res_list[4]

    fft1 =  np.absolute(scipy.fft.rfft(ch1))
    fft2 =  np.absolute(scipy.fft.rfft(ch2))
            
    #Actualizar la data
    curve.setData(ch1)
    curve2.setData(ch2)

    curve3.setData(fft1)
    curve4.setData(fft2)

    f, t, Sxx = scipy.signal.spectrogram(ch1, fs=250, nperseg=64)
    img.setImage(Sxx)
    bar.setImageItem(img)
    bar.setLevels([Sxx.min(), Sxx.max()])
    
    f, t, Sxx2 = scipy.signal.spectrogram(ch2, fs=250, nperseg=64)
    img2.setImage(Sxx2)
    bar2.setImageItem(img2)
    bar2.setLevels([Sxx2.min(), Sxx2.max()])

#--------------------------------------------------------------------------------------

def main():
    #Declaration of variables
    ptr = 0
    n = 200
    ch1 = np.zeros(n)
    ch2 = np.zeros(n)
    
    #Open COM port
    s = serial.Serial(port='COM3', baudrate=57600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None, exclusive=None) 

    print('Starting...')
    #Bytes defined by SMT-EEG as sync bytes
    start_bytes =  b'\xa5\x5a\x02' #sync0 + sync1 + version

    win = generate_window()
    
    #creation of window and plots
    eeg_plot1, curve_plot1 = generate_plot('channel 1 in real time: Plotting', [0,100], [-200,1200], win)
    eeg_plot2, curve_plot2 = generate_plot('Canal 2 in real time: Plotting', [0,100], [-200,1200], win)
    
    win.nextRow()
    
    fft_plot1, curve_fft1 = generate_plot('channel 1 fourier in real time: Plotting', [0,100], [0,8000], win)
    fft_plot2, curve_fft2 = generate_plot('Canal 2 fourier in real time: Plotting', [0,100], [0,8000], win)
    
    win.nextRow()

    bar, img = generate_colorBarItem("Spectogram ch1", win)
    bar2, img2 = generate_colorBarItem("Spectogram ch2", win)

    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: update(s, start_bytes, n, ch1, ch2, fft_plot1, fft_plot2, curve_plot1, curve_plot2, curve_fft1, curve_fft2, img, bar, img2, bar2))

    #Milliseconds interval between data updates
    timer.start(500)
    pg.exec()

#--------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
    