import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QGraphicsWidget
from PyQt5.QtChart   import QChart, QLineSeries
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from views.robotCtrlUi import robotCtrlUi
from util.manipulator import Manipulator
# from views.robotCtrlUi import ScrollingTimestampPlot


import os
from PyQt5 import uic

#class View(QWidget):
class View(QMainWindow):
    def __init__(self,  controller, model):
        print("main_view: Init")
        super(View, self).__init__()

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self._ui = uic.loadUi(os.path.join("D:/NCKH/AppQt/Project/ArmGUI/", "resources/mainwindow.ui"), self)
        #self._ui = loadUi("resources/mainwindow.ui", self)
        self._controller = controller
        self._model = model
        self._robotCtrlUi = robotCtrlUi(self._ui)
        self._robotCalculate = Manipulator(0,0,0)

        # scrolling_timestamp_plot_widget = ScrollingTimestampPlot()
        #
        #
        # self.addLayout(scrolling_timestamp_plot_widget.get_scrolling_timestamp_plot_layout(), 0, 0)

        # connect ui-widget to controller
        # if ui changes, it sends a signal to an slot on which we connect a controller class.
        # therefore we can recive the signal in the controller
        self._ui.connectBtn.clicked.connect(self.getUsbInfoFromGUI)
        self._ui.movPosBtn.clicked.connect(self.getPosistion)
        self._ui.movHomeBtn.clicked.connect(lambda: self._controller.moveHome)
        self._ui.movConveyorBtn.clicked.connect(self.setConveyorSpeed)
        self._ui.movJointBtn.clicked.connect(self.getJointAngle)

        self._ui.DetectButton.clicked.connect(lambda: self._controller.startDetectionTimer())
        self._ui.StopButton.clicked.connect(lambda: self._controller.endDetectionTimer())

        # listen for model event signals
        # connect the method to update the ui to the slots of the model
        # if model sends/emits a signal the ui gets notified
        self._model.usbInfoChanged.connect(self.onUsbInfoChangeEvent)
        self._model.cameraDetectImgChanged.connect(self.onCameraImgDectectChangeEvent)
        self._model.motorCurrentGraphChanged.connect(self.onMotorCurrentGraphChangeEvent)

    def onMotorCurrentGraphChangeEvent(self, value):
        self._robotCtrlUi.uiUpdateGraph(value)

    def onCameraImgDectectChangeEvent(self, imgPath):
        print(imgPath)
        self.imgLabel.setPixmap(QPixmap(imgPath))
        self.imgLabel.setScaledContents(True)

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
                print("usb went wrong")
            else:
                print("At least one field (VID, PID) is empty")

    def setPosistion(self, x, y, z):
        self._ui.x_txt.setPlainText(str(x))
        self._ui.y_txt.setPlainText(str(y))
        self._ui.z_txt.setPlainText(str(z))

    def getPosistion(self):
        try:
            self._controller.movePos(float(self._ui.x_txt.toPlainText()),
                                     float(self._ui.y_txt.toPlainText()),
                                     float(self._ui.z_txt.toPlainText()))
            joint = self._robotCalculate.inverseKinematics(float(self._ui.x_txt.toPlainText()),
                                                 float(self._ui.y_txt.toPlainText()),
                                                 float(self._ui.z_txt.toPlainText()))
            self.setJointAngle(joint[0], joint[1], joint[2])
            self.setJointSlider(joint[0], joint[1], joint[2])

        except:
            if str(self._ui.x_txt.toPlainText()) != "" and str(self._ui.y_txt.toPlainText()) != "" \
                    and str(self._ui.z_txt.toPlainText()) != "":
                print("posistion went wrong")
            else:
                print("At least one field of coordinate posistion is empty")

    def setJointAngle(self, q1, q2, q3):
        self._ui.joint1_txt.setPlainText(str(q1))
        self._ui.joint2_txt.setPlainText(str(q2))
        self._ui.joint3_txt.setPlainText(str(q3))

    def setJointSlider(self, q1, q2, q3):
        self._ui.joint1_slider.setValue(q1)
        self._ui.joint2_slider.setValue(q2)
        self._ui.joint3_slider.setValue(q3)

    def getJointAngle(self):
        try:
            self._controller.moveJoint(float(self._ui.joint1_txt.toPlainText()),
                                     float(self._ui.joint2_txt.toPlainText()),
                                     float(self._ui.joint3_txt.toPlainText()))
            pos = self._robotCalculate.forwardKinematics(float(self._ui.joint1_txt.toPlainText()),
                                                           float(self._ui.joint2_txt.toPlainText()),
                                                           float(self._ui.joint3_txt.toPlainText()))
            self.setPosistion(pos[0], pos[1], pos[2])

        except:
            print("At least one field of joint angle is empty")

    def setConveyorSpeed(self):
        try:
            if (self._ui.mode_con_txt.currentText()):
                self._controller.moveConveyor(float(self._ui.set_speed_con_txt.toPlainText()), str(self._ui.mode_con_txt.currentText()))

        except:
            if str(self._ui.set_speed_con_txt.toPlainText()) != "":
                print("something went wrong")
            else:
                print("At least one field of conveyor is empty")