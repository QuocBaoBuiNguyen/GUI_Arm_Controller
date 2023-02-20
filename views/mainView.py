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

        self._ui = loadUi("resources/mainwindow.ui", self)

        self._controller = controller
        self._model = model
        self._robotCtrlUi = robotCtrlUi(self._ui)

        # connect ui-widget to controller
        # if ui changes, it sends a signal to an slot on which we connect a controller class.
        # therefore we can recive the signal in the controller
        self.connectBtn.clicked.connect(self.getUsbInfoFromGUI)
        self._ui.movPosBtn.clicked.connect(self.getPosistion)
        self._ui.movJointBtn.clicked.connect(self.getJointAngle)

        # listen for model event signals
        # connect the method to update the ui to the slots of the model
        # if model sends/emits a signal the ui gets notified
        self._model.usbInfoChanged.connect(self.onUsbInfoChangeEvent)

    def onUsbInfoChangeEvent(self, usbConnStatus):
        if usbConnStatus:
            self._ui.connectBtn.setText("Disconnect")
            self._ui.usbStatusLabel.setText("Connected")
        else:
            self._ui.connectBtn.setText("Connect")
            self._ui.usbStatusLabel.setText("Disconnected")

    def getUsbInfoFromGUI(self):
        try:
            self._controller.usbConnect(int(self._ui.vidTxt.toPlainText()), int(self._ui.pidTxt.toPlainText()))
        except:
            if str(self._ui.vidTxt.toPlainText()) != "" and str(self._ui.pidTxt.toPlainText()) != "":
                print("something went wrong")
            else:
                print("At least one field (VID, PID) is empty")
    def getPosistion(self):
        try:
            self._controller.movePos(float(self._ui.x_txt.toPlainText()),
                                     float(self._ui.y_txt.toPlainText()),
                                     float(self._ui.z_txt.toPlainText()))
        except:
            if str(self._ui.x_txt.toPlainText()) != "" and str(self._ui.y_txt.toPlainText()) != "" \
                    and str(self._ui.z_txt.toPlainText()) != "":
                print("something went wrong")
            else:
                print("At least one field of coordinate posistion is empty")

    def getJointAngle(self):
        try:
            self._controller.moveJoint(float(self._ui.joint1_txt.toPlainText()),
                                     float(self._ui.joint2_txt.toPlainText()),
                                     float(self._ui.joint3_txt.toPlainText()))
        except:
            print("At least one field of joint angle is empty")
