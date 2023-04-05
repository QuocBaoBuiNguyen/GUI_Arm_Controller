from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QGraphicsScene, QApplication, QDialog, QMainWindow, QGraphicsWidget
from PyQt5.QtChart import QChart, QLineSeries, QValueAxis
from pyqtgraph import PlotWidget, plot
from PyQt5.QtCore import *
import pyqtgraph as pg
from threading import Thread
from collections import deque
import random
import time

class robotCtrlUi():
    def __init__(self, resource):

        self.MAX_BYTE_DISPLAY = 500
        self._uiResource = resource
        self._uiResource.graphicsView.setBackground('w')
        
        # Add Title
        self._uiResource.graphicsView.setTitle("Encoder value of each joint motor", font="Miriam Fixed", color="black", size="10pt")
        # Add Axis Labels
        styles = {"color": "#000", "font-size": "15px"}
        self._uiResource.graphicsView.setLabel("left", "Degree (°)", **styles)
        self._uiResource.graphicsView.setLabel("bottom", "Time (secs)", **styles)
        # Add legend
        self._uiResource.graphicsView.addLegend()
        
        self._uiResource.graphicsView.plotItem.setMouseEnabled(x=False, y=False)
        self.time = list(range(self.MAX_BYTE_DISPLAY))  # 100 time points
        self.motor1 = [32768 for _ in range(self.MAX_BYTE_DISPLAY)]  # 100 data points
        self.motor2 = [32768 for _ in range(self.MAX_BYTE_DISPLAY)]  # 100 data points
        self.motor3 = [32768 for _ in range(self.MAX_BYTE_DISPLAY)]  # 100 data points

        pen = pg.mkPen(color=(255, 0, 0))
        self._uiResource.graphicsView.showGrid(x=True, y=True)

        self.data_line1 = self.plot(self.time, self.motor1, "Motor1", 'r')
        self._uiResource.motor1_lbl.setStyleSheet("QLabel {color : red; }")
        self.data_line2 = self.plot(self.time, self.motor2, "Motor2", 'b')
        self._uiResource.motor2_lbl.setStyleSheet("QLabel { color : blue; }")
        self.data_line3 = self.plot(self.time, self.motor2, "Motor2", 'g')
        # self._uiResource.motor3_lbl.setStyleSheet("QLabel { color : green; }")

        self.processingData = False;

        # self.timer = QtCore.QTimer()
        # self.timer.setInterval(50)
        # self.timer.timeout.connect(self.update_plot_data)
        # self.timer.start()

    def plot(self, time, y, plotname, color):
        pen = pg.mkPen(color=color)
        return self._uiResource.graphicsView.plot(time, y, name=plotname, pen=pen, symbol='+', symbolSize=7, symbolBrush=(color))

    def uiUpdateGraph(self, value):
        self.processingData = True;
        print(len(self.motor1))
        print(len(self.motor2))
        print(len(self.motor3))

        if len(self.motor1) == self.MAX_BYTE_DISPLAY:
            self.motor1 = self.motor1[1:]  # Remove the first

        if len(self.motor2) == self.MAX_BYTE_DISPLAY:
            self.motor2 = self.motor2[1:]  # Remove the first

        if len(self.motor3) == self.MAX_BYTE_DISPLAY:
            self.motor3 = self.motor3[1:]  # Remove the first

        self.motor1.append(int(value[0][0]))
        self.motor2.append(int(value[1][0]))
        self.motor3.append(int(value[2][0]))


        self.time = self.time[1:]  # Remove the first y element.
        self.time.append(self.time[-1] + 1)  #

        print(len(self.motor1))
        print(len(self.motor2))
        print(len(self.motor3))
        print(len(self.time))

        self.data_line1.setData(self.time, self.motor1)  # Update the data.
        self.data_line2.setData(self.time, self.motor2)  # Update the data.
        self.data_line3.setData(self.time, self.motor3)  # Update the data.
        self.processingData = False;

    def update_line_data(self, motor_data, _time, data_line):
        motor_data = motor_data[1:]  # Remove the first
        motor_data.append(random.randint(0, 100))  # Add a new random value.
        data_line.setData(_time, motor_data)  # Update the data.

    def update_plot_data(self):
        if self.processingData == False:
            print("HEHEHE")
            print("CJAJAJA" ,len(self.motor1))
            print(len(self.motor2))
            print(len(self.motor3))

            # self.time = self.time[1:]  # Remove the first y element.
            # self.time.append(self.time[-1] + 1)  # Add a new value 1 higher than the last.
            #
            # # self.update_line_data(self.motor1, self.time, self.data_line1)
            # # self.update_line_data(self.motor2, self.time, self.data_line2)
            #
            # # self.motor1 = self.motor1[1:]  # Remove the first
            # # self.motor1.append(random.randint(0, 500))  # Add a new random value.
            self.data_line1.setData(self.time, self.motor1)  # Update the data.
            #
            # # self.motor2 = self.motor2[1:]  # Remove the first
            # # self.motor2.append(random.randint(0, 100))  # Add a new random value.
            self.data_line2.setData(self.time, self.motor2)  # Update the data.
            #
            # # self.motor3 = self.motor3[1:]  # Remove the first
            # # self.motor3.append(random.randint(0, 100))  # Add a new random value.
            self.data_line3.setData(self.time, self.motor3)  # Update the data.

        # self.ui = resource
        #
        # self.DATA_POINTS_TO_DISPLAY = 200
        # self.FREQUENCY = 2.5
        # self.SCROLLING_TIMESTAMP_PLOT_REFRESH_RATE = self.FREQUENCY * self.MAX_BYTE_DISPLAY
        #
        # self.motorArr1 = deque(maxlen=self.DATA_POINTS_TO_DISPLAY)
        # self.motorArr2 = deque(maxlen=self.DATA_POINTS_TO_DISPLAY)
        # self.motorArr3 = deque(maxlen=self.DATA_POINTS_TO_DISPLAY)
        # self.data = deque(maxlen=self.DATA_POINTS_TO_DISPLAY)
        #
        # self.seriesMotor1 = QLineSeries()
        # self.seriesMotor2 = QLineSeries()
        # self.seriesMotor3 = QLineSeries()
        # self.seriesData =  QLineSeries()
        #
        # # self.loadMotor1Series()
        # # self.loadMotor2Series()
        # # self.loadMotor3Series()
        # self.jointChart = QChart()
        #
        # self.jointChart.addSeries(self.seriesMotor1)
        # self.jointChart.addSeries(self.seriesMotor2)
        # self.jointChart.addSeries(self.seriesMotor3)
        # self.jointChart.addSeries(self.seriesData)
        #
        # self.jointChart.setTitle('Current joint angle')
        #
        # y_axis = QValueAxis()
        # y_axis.setRange(0, 10)
        # # y_axis.setLabelFormat("%0.1f")
        # # y_axis.setTickCount(1)
        # # y_axis.setMinorTickCount(0)
        # # y_axis.setTickType(QValueAxis.TickType.TicksDynamic)
        # # y_axis.setTickInterval(1)
        # y_axis.setTitleText("Encoder Value")
        #
        # x_axis = QValueAxis()
        # x_axis.setRange(1, len(self.data))
        # x_axis.setLabelFormat("%d")
        # x_axis.setTickCount(1)
        # x_axis.setMinorTickCount(1)
        # #
        # # x_axis.setRange(1, self.seriesMotor1.count())
        # # x_axis.setLabelFormat("%d")
        # # y_axis.setTickType(QValueAxis.TickType.TicksDynamic)
        # # y_axis.setTickInterval(1)
        # x_axis.setTitleText("Current time")
        #
        # self.jointChart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        # self.jointChart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)
        # self.jointChart.legend().setVisible(True)
        # self.ui.graphicsView.setChart(self.jointChart)
        #
        # self.timestamp = QtCore.QTime()
        # self.timestamp.start()
        #
        # self.read_position_thread()
        # self.start()

    def start(self):
        """Update plot"""
        self.position_update_timer = QtCore.QTimer()
        self.position_update_timer.timeout.connect(self.plot_updater)
        self.position_update_timer.start(self.get_scrolling_timestamp_plot_refresh_rate())

    def read_position_thread(self):
        self.current_position_value = 0
        self.position_update_thread = Thread(target=self.read_position, args=())
        self.position_update_thread.daemon = True
        self.position_update_thread.start()

    def get_scrolling_timestamp_plot_refresh_rate(self):
        return self.SCROLLING_TIMESTAMP_PLOT_REFRESH_RATE

    def plot_updater(self):
        self.data_point = float(self.current_position_value)

        self.data.append({'x': self.timestamp.elapsed(), 'y': self.data_point})
        self.loadData()
        # print(self.data)
        # self.seriesData.append(x=[item['x'] for item in self.data], y=[item['y'] for item in self.data])

    def read_position(self):
        frequency = self.FREQUENCY
        while True:
            self.current_position_value = random.randint(0, 10)
            time.sleep(frequency)

    def loadData(self):
        for index, element in enumerate(self.data):
            print(element["x"])
            self.seriesMotor1.append(element["x"], element["y"])
        self.seriesMotor1.setName('Encoder DC motor 1')


    # def loadMotor1Series(self):
    #     for index, element in enumerate(self.motorArr1):
    #         image_num = index + 1
    #         print(image_num,  element)
    #         self.seriesMotor1.append(image_num, element)
    #     self.seriesMotor1.setName('Encoder DC motor 1')
    #
    # def loadMotor2Series(self):
    #     for index, element in enumerate(self.motorArr2):
    #         image_num = index + 1
    #         self.seriesMotor2.append(image_num, element)
    #     self.seriesMotor2.setName('Encoder DC motor 2')
    #
    # def loadMotor3Series(self):
    #     for index, element in enumerate(self.motorArr3):
    #         image_num = index + 1
    #         self.seriesMotor3.append(image_num, element)
    #     self.seriesMotor3.setName('Encoder DC motor 3')
    #
    # def uiUpdateGraph(self, value):
    #     self.motorArr1.append(value[0])
    #     self.motorArr2.append(value[1])
    #     self.motorArr3.append(value[2])
    #     self.loadMotor1Series()
    #     # self.loadMotor2Series()
    #     # self.loadMotor3Series()
    #     self.x_axis.setRange(1, len(self.motorArr1))
    #     self.ui.graphicsView.update()

    # def drawChart(self):

