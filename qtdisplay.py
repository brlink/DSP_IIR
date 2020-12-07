import numpy as np
from pyqtgraph.widgets.GroupBox import GroupBox
import scipy.signal as signal

#import QT
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtWidgets import QLabel, QLineEdit, QCheckBox

#import filters
import IIRFilter


class QtDisplay:

    def __init__(self, title, sampling_rate):

        # add variable for caculate:
        self.win = pg.GraphicsLayoutWidget()
        # set window title
        self.win.setWindowTitle(title)
        # set window background
        self.win.setBackground('w')
        self.layout = QtGui.QGridLayout()

        # data and filter for calculating
        self.data_speed = 0
        # store data no processed
        self.data_orign = []
        # store data processed
        self.data_processed = []
        # self.data_display = []

        # design filter:
        ## highpass above 0.5hz
        self.filter_highpass = IIRFilter.IIRFilter(signal.cheby2(8, 40, 0.5 / sampling_rate * 2, 
                                        btype='highpass', 
                                        output='sos'))

        ## lowpass below 40hz
        self.filter_lowpass = IIRFilter.IIRFilter(signal.cheby2(4, 60, 40 / sampling_rate *2, 
                                        btype='lowpass', 
                                        output='sos'))

        # add widgets in qt window
        self.plt = pg.PlotWidget(background='w')
        self.plt.setYRange(0, 1)
        self.plt.setXRange(0, 500)
        self.plt.setMouseEnabled(x=False, y=False)
        self.curve = self.plt.plot()

        # add Radio buttons
        self.select_box = GroupBox("filters")
        self.select_boxlayout = QtGui.QGridLayout()
        # self.rb_lfilter10 = QCheckBox("Lowpass 10Hz")
        self.rb_hfilter40 = QCheckBox("Lowpass 40Hz")
        # self.rb_lfilter10.setChecked(True)
        self.rb_hfilter40.setChecked(True)
        # self.select_boxlayout.addWidget(self.rb_lfilter10, 0, 0)
        self.select_boxlayout.addWidget(self.rb_hfilter40, 0, 0)
        self.select_box.setLayout(self.select_boxlayout)
        
        # add output text
        self.output_box = GroupBox("Output")
        self.label = QLabel()
        self.label.setText("ready for starting filtering")
        self.output_line = QLineEdit()
        self.output_boxlayout = QtGui.QGridLayout()
        self.output_boxlayout.addWidget(self.label, 0, 0)
        self.output_box.setLayout(self.output_boxlayout)
        
        # add timer to refresh
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        # set layout 
        self.layout.addWidget(self.plt, 0, 0)
        self.layout.addWidget(self.select_box, 1, 0)
        self.layout.addWidget(self.output_box, 3, 0)


        self.win.setLayout(self.layout)
        self.win.show()


    def update(self):
        self.data_orign = self.data_orign[-500 : ]
        self.data_processed = self.data_processed[-500 : ]
        # self.data_display = 20* np.log(self.data_processed)
    
        if self.data_processed:
            self.plt.setYRange(0, 1)
            self.curve.setData(np.hstack(self.data_processed))
        
        if not self.rb_hfilter40.isChecked():
            self.label.setText("filtering not completely")
        else:
            self.label.setText("the lowpass filter {}Hz start".format(40))
    

    def addData(self, raw_data):

        self.data_orign.append(raw_data)
        handled_data = raw_data
        
        # enable highpass
        # if self.rb_lfilter10.isChecked():
        #     handled_data = self.filter_highpass.filter(handled_data)
        if self.rb_hfilter40.isChecked():
        # enable lowpass
            handled_data = self.filter_lowpass.filter(handled_data)
        
        # if self.rb_lfilter10.isChecked() and self.rb_hfilter40.isChecked():
        #     # pass
        #     pass
        
        
        # impelement
        self.data_processed.append(handled_data)