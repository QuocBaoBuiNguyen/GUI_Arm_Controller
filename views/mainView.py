import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QGraphicsWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtChart   import QChart, QLineSeries
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from views.robotCtrlUi import robotCtrlUi

import os
from PyQt5 import uic

import datetime

#class View(QWidget):
class View(QMainWindow):

    id = 0
    pickedUp = 1
    price = 0

    def __init__(self,  controller, model):
        print("main_view: Init")
        super(View, self).__init__()

        ui_path = os.path.dirname(os.path.abspath(__file__))
        self._ui = uic.loadUi(os.path.join("E:\HCMUT\FinalProject\GUI\GUI_Arm_Controller", "resources/mainwindow.ui"), self)
        #self._ui = loadUi("resources/mainwindow.ui", self)
        self._controller = controller
        self._model = model
        self._robotCtrlUi = robotCtrlUi(self._ui)

        #set label for data table( not done yet )
        header = self.SQLtableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.SQLtableWidget.setHorizontalHeaderLabels(['Id', 'Name', 'Price', 'DateTime'])

        # connect ui-widget to controller
        # if ui changes, it sends a signal to an slot on which we connect a controller class.
        # therefore we can recive the signal in the controller
        self._ui.connectBtn.clicked.connect(self.getUsbInfoFromGUI)
        self._ui.movPosBtn.clicked.connect(self.getPosistion)
        self._ui.movHomeBtn.clicked.connect(lambda: self._controller.moveHome())
        self._ui.movJointBtn.clicked.connect(self.getJointAngle)

        self._ui.DetectButton.clicked.connect(lambda: self._controller.startDetectionTimer())
        self._ui.StopButton.clicked.connect(lambda: self._controller.endDetectionTimer())

        # listen for model event signals
        # connect the method to update the ui to the slots of the model
        # if model sends/emits a signal the ui gets notified
        self._model.usbInfoChanged.connect(self.onUsbInfoChangeEvent)
        self._model.cameraDetectImgChanged.connect(self.onCameraImgDectectChangeEvent)

        self._ui.SQLBtn.clicked.connect(self.onSQLpushButtonChangeEvent)
        self._ui.SQLSaveBtn.clicked.connect(self.onSQLSaveButtonChangeEvent)
        self._ui.DeleteDataBtn.clicked.connect(self.onDeleteData)

        # robot have picked up object and return it label
        self.label = "Monster"
        print(self.label)
        self._ui.pickupBtn.clicked.connect(self.onPickedupSignal)

    def onDeleteData(self):
        self._controller.deleteSQLData()
        self.onSQLpushButtonChangeEvent()
        self.id = 0

    def onPickedupSignal(self):
        self.switchPickedUpVar()
        # self.label = "Pepsi"
        print(self.label)
        if self.label == "Pepsi":
            self.price = 10000
        elif self.label == "Monster":
            self.price = 20000
        elif self.label == "Starbuck":
            self.price == 30000
        if self.pickedUp == 1:
            self.id += 1
            self.currentTime = self.getCurrentTime()
            print(str(self.id), self.label, str(self.price), self.currentTime)
            self.savepickupdatatoSQL(str(self.id), self.label, str(self.price), self.currentTime)

    def switchPickedUpVar(self):
        print("switchPickedUpVar called")
        if self.pickedUp == 0:
            self.pickedUp = 1
        else:
            self.pickedUp = 0
        print('Variable:', self.pickedUp)

    def getCurrentTime(self):
        #get current time
        current_date_time = datetime.datetime.now()
        formatted_date_time = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
        print("Current date and time:", formatted_date_time)
        return formatted_date_time

    def onSQLSaveButtonChangeEvent(self):
        self.id += 1
        self.currentTime = self.getCurrentTime()
        self._controller.insertSQLData(str(self.id), "Pepsi", "10000", self.currentTime)
        self.onSQLpushButtonChangeEvent()

    def savepickupdatatoSQL(self, Id, Name, Price, DateandTime):
        print("savepickupdatatoSQL called")
        self._controller.insertSQLData(Id, Name, Price, DateandTime)
        self.onSQLpushButtonChangeEvent()


    def onSQLpushButtonChangeEvent(self):
        print("onSQLpushButtonChangeEvent called")
        # self._controller.loadSQLData
        self.result = self._controller.loadSQLData()
        # print(self.result)
        self.SQLtableWidget.setRowCount(0)
        for row_num, row_data in enumerate(self.result):
            self.SQLtableWidget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                self.SQLtableWidget.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(col_data)))


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
