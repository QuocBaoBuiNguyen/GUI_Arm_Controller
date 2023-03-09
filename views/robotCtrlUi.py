from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QGraphicsWidget
from PyQt5.QtChart   import QChart, QLineSeries, QValueAxis
from PyQt5.QtCore import *

class robotCtrlUi():
    def __init__(self, resource):
        self.ui = resource

        self.array_average = [28.284563290387887, 28.170853249077403, 28.776281519708895, 29.041099232443074, 29.232627358676552]
        self.array_max = [33.4762780011805, 33.4762780011805, 33.61541095358507, 33.929353828043304, 33.929353828043304]
        self.array_min = [20.46583000704794, 20.288281209883735, 20.772403295556217, 21.20685421472882, 21.625995561649745]

        self.jointChart = QChart()
        self.series_average = QLineSeries()
        self.series_max = QLineSeries()
        self.series_min = QLineSeries()

        self.loadSerie_average()
        self.loadSerie_max()
        self.loadSerie_min()

        self.jointChart.addSeries(self.series_average)
        self.jointChart.addSeries(self.series_max)
        self.jointChart.addSeries(self.series_min)

        self.jointChart.setTitle('Current joint angle')
        # self.jointChart.createDefaultAxes()

        y_axis = QValueAxis()
        y_axis.setRange(24.0, 39.0)
        y_axis.setLabelFormat("%0.2f")
        # y_axis.setTickCount(1)
        # y_axis.setMinorTickCount(0)
        y_axis.setTickType(QValueAxis.TickType.TicksDynamic)
        y_axis.setTickInterval(1)
        y_axis.setTitleText("Encoder Value")

        x_axis = QValueAxis()
        # x_axis.setRange(1, len(self.array_average))
        # x_axis.setLabelFormat("%d")
        # x_axis.setTickCount(1)
        # x_axis.setMinorTickCount(1)
        #
        x_axis.setRange(1, self.series_average.count())
        x_axis.setLabelFormat("%d")
        y_axis.setTickType(QValueAxis.TickType.TicksDynamic)
        y_axis.setTickInterval(1)
        x_axis.setTitleText("Current time")

        self.jointChart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.jointChart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)
        self.jointChart.legend().setVisible(True)
        self.jointChart.addSeries(self.series_average)
        self.jointChart.addSeries(self.series_max)
        self.jointChart.addSeries(self.series_min)

        self.ui.graphicsView.setChart(self.jointChart)

    def loadSerie_average(self):
        for index, element in enumerate(self.array_average):
            image_num = index + 1
            self.series_average.append(image_num, element)
        self.series_average.setName('Encoder DC motor 1')

    def loadSerie_max(self):
        for index, element in enumerate(self.array_max):
            image_num = index + 1
            self.series_max.append(image_num, element)
        self.series_max.setName('Encoder DC motor 2')

    def loadSerie_min(self):
        for index, element in enumerate(self.array_min):
            image_num = index + 1
            self.series_min.append(image_num, element)
        self.series_min.setName('Encoder DC motor 3')