import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QGraphicsWidget
from PyQt5.QtChart   import QChart, QLineSeries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from views.robotCtrlUi import robotCtrlUi

#class View(QWidget):
class View(QMainWindow):

    def __init__(self,  controller, model):
        print("main_view: Init")
        super(View, self).__init__()

        self._ui = loadUi("resources/main.ui", self)

        self._controller = controller
        self._model = model
        self._robotCtrlUi = robotCtrlUi(self._ui)

        # self.connectBtn.clicked.connect(lambda: self._controller.usbConnect(int(self._ui.vidTxt.toPlainText()),
        #                                                                     int(self._ui.pidTxt.toPlainText())))
        self.connectBtn.clicked.connect(lambda: self._controller.usbConnect(1155, 22336))

        self._ui.movCmdBtn.clicked.connect(self.getPosistion)

    def getPosistion(self):
        # if str(self._ui.x_txt.toPlainText()) != "" and str(self._ui.y_txt.toPlainText()) != "" and str(self._ui.z_txt.toPlainText()) != "":
            self._controller.moveCmd(float(self._ui.x_txt.toPlainText()),
                                     float(self._ui.y_txt.toPlainText()),
                                     float(self._ui.z_txt.toPlainText()))
        # else:
        #     print("At least one field of coordinate posistion is empty")

