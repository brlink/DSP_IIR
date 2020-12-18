import numpy as np
from pyqtgraph.widgets.GroupBox import GroupBox
from pyqtgraph.functions import mkPen, pseudoScatter

import scipy.signal as signal
import time

#import QT
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from PyQt5.QtWidgets import QLabel, QLineEdit, QCheckBox

#import filters
import IIRFilter


class Detector:
    """a class to detect whether a computer is closed or opened"""

    def __init__(self):
        self.data_pre = 0  # data buffer of the previous one
        self.drop = 0  # the total light drop

    def detect(self, new_data):
        # drop
        self.drop = (self.data_pre - new_data)

        if np.abs(self.drop) < 0.2:
            return 0
        else:
            # drop < 0, means open
            if self.drop < 0:
                self.update(new_data)
                return 1
            else:  # drop > 0, means close
                self.update(new_data)
                return -1

    def clean(self):
        # clean all the data of this detector
        self.drop = 0
        self.data_pre = 0

    def update(self, new_data):
        # update previous data
        self.data_pre = new_data


class QtDisplay:

    def __init__(self, title, sampling_rate):

        # add variable for caculate:
        self.win = pg.GraphicsLayoutWidget()
        # set window title
        self.win.setWindowTitle(title)
        # set window background
        self.win.setBackground('w')
        self.layout = QtGui.QGridLayout()

        # # data and filter for calculating
        # self.data_speed = 0
        # store data no processed
        self.data_orign = []
        # store data processed
        self.data_processed = []
        # self.data_display = []

        # initial detector
        self.detector = Detector()

        # design filter:
        # highpass above 0.5hz
        self.filter_highpass = IIRFilter.IIRFilter(signal.cheby2(8, 40, 0.5 / sampling_rate * 2,
                                                                 btype='highpass',
                                                                 output='sos'))

        # lowpass below 40hz
        self.filter_lowpass = IIRFilter.IIRFilter(signal.cheby2(4, 60, 36 / sampling_rate * 2,
                                                                btype='lowpass',
                                                                output='sos'))

        # add widgets in qt window
        self.plt = pg.PlotWidget(background='k')
        self.plt.setYRange(0, 0.5)
        self.plt.setXRange(0, 500)
        self.plt.setMouseEnabled(x=False, y=False)
        pen_line = mkPen(width=5, color='EE7942')
        pen_axis = mkPen(width=3, color='FFFFFF')
        self.plt.getAxis('bottom').setPen(pen_axis)
        self.plt.getAxis('bottom').setTextPen(pen_axis)
        self.plt.getAxis('left').setPen(pen_axis)
        self.plt.getAxis('left').setTextPen(pen_axis)
        self.curve = self.plt.plot(pen=pen_line)

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
        self.data_orign = self.data_orign[-500:]
        self.data_processed = self.data_processed[-500:]
        # self.data_display = 20* np.log(self.data_processed)

        if self.data_processed:
            self.plt.setYRange(0, 0.5)
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

            stat = self.detector.detect(handled_data)

            seconds = time.time()
            now = time.ctime(seconds)

            if stat == 0:
                pass
            if stat == -1:
                # add data to log file
                log_file = open("detector.log", 'a')
                log_file.write("Laptop close at {}\n".format(now))
                log_file.close()
            if stat == 1:
                # add data to log file
                log_file = open("detector.log", 'a')
                log_file.write("Laptop open at {}\n".format(now))
                log_file.close()
        else:
            self.detector.clean()

        # if self.rb_lfilter10.isChecked() and self.rb_hfilter40.isChecked():
        #     # pass
        #     pass

        # impelement
        self.data_processed.append(handled_data)
