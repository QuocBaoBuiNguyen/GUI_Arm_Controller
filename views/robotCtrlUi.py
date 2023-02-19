from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QGraphicsWidget
from PyQt5.QtChart   import QChart, QLineSeries
from PyQt5.QtCore import *

class robotCtrlUi():
    def __init__(self, resource):
        self.ui = resource
        jointChart = QChart()
        series = QLineSeries()

        series.append(1, 3)
        series.append(2, 4)

        jointChart.addSeries(series)
        jointChart.setTitle('Example')
        jointChart.createDefaultAxes()
        self.ui.graphicsView.setChart(jointChart)

    def getPID(self):
        return self.ui.pidTxt.toPlainText()
    def getVID(self):
        return self.ui.vidTxt.toPlainText()

