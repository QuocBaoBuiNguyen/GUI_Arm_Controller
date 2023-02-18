import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QGraphicsWidget
from PyQt5.QtChart   import QChart, QLineSeries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

#class View(QWidget):
class View(QMainWindow):
    def __init__(self, model, main_ctrl):
        print("main_view: Init")
        super(View, self).__init__()
        self._mainCtrl = main_ctrl;
        self.mainUI()
        #self.tabUI()

    # def menuUI(self):
    #     QWidget.__init__(self)
    #     layout = QGridLayout()
    #     self.setLayout(layout)
    #
    #     # create menu
    #     menubar = QMenuBar()
    #     layout.addWidget(menubar, 0, 0)
    #     actionFile = menubar.addMenu("File")
    #     actionFile.addAction("New")
    #     actionFile.addAction("Open")
    #     actionFile.addAction("Save")
    #     actionFile.addSeparator()
    #     actionFile.addAction("Quit")
    #     menubar.addMenu("Edit")
    #     menubar.addMenu("View")
    #     menubar.addMenu("Help")
    #
    #     # add textbox
    #     tbox = QPlainTextEdit()
    #     layout.addWidget(tbox, 1, 0)
    #
    # def tabUI(self):
    #     QWidget.__init__(self)
    #     layout = QGridLayout()
    #     self.setLayout(layout)
    #     label1 = QLabel("Widget in Tab 1.")
    #     label2 = QLabel("Widget in Tab 2.")
    #     tabwidget = QTabWidget()
    #     tabwidget.addTab(label1, "Tab 1")
    #     tabwidget.addTab(label2, "Tab 2")
    #     layout.addWidget(tabwidget, 0, 0)

    def mainUI(self):
        chart = QChart()
        series = QLineSeries()

        series.append(1, 3)
        series.append(2, 4)

        chart.addSeries(series)
        chart.setTitle('Example')
        chart.createDefaultAxes()

        # Ham loadUi nay chi lien quan den viec dua du lieu vao self
        # de lay ra graphicView cho khong lien quan den render ra man hinh
        # nen de trong day cung duoc
        loadUi("resources/newUI.ui", self)
        self.graphicsView.setChart(chart)
        # Ham nay de dang ki
        self.connectBtn.clicked.connect(self._mainCtrl.usbConnect)


