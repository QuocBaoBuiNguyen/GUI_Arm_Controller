import array as arr
from controllers.usbController import UsbController
from controllers.cameraController import CameraController
from util.dataTypes import arrayFloat
import struct
import time #for test

class Controller(object):
    def __init__(self, model):
        print("main_ctrl: Init")
        self._model = model
        self._usbCtrl = UsbController(self.receiveUsbEventHandler)
        self._cameraCtrl = CameraController(self.photoCaptureEventCb, self.chosePosDependOnLabel)

    def photoCaptureEventCb(self, imagePath):
        self._model.cameraCurrImg = imagePath

    def startDetectionTimer(self):
        self._cameraCtrl.start_capture_video()

    def endDetectionTimer(self):
        self._cameraCtrl.stop_capture_video()

    def receiveUsbEventHandler(self, serialByte):
        frameList = list(serialByte)
        print("Main Controller: Receive ", frameList)

        if frameList[0] == self._usbCtrl.STX and frameList[21] == self._usbCtrl.ETX:
            if frameList[20] == self._usbCtrl.ACK:
                cmd = ''.join(map(str, ''.join(chr(i) for i in frameList[1:5])))
                print("Main Controller: Receive cmd:", cmd)
                if cmd == 'RCPG':
                    # Run finish process
                    print('RCPG')
                elif cmd == 'SPOS':
                    joint_angle1 = self.convert_from_byte(frameList[8:12])
                    joint_angle2 = self.convert_from_byte(frameList[12:16])
                    joint_angle3 = self.convert_from_byte(frameList[16:20])
                    self._model.motorGraphCurr = [joint_angle1, joint_angle2, joint_angle3]

    def convert_from_byte(self, data):
        results = []
        while data:
            part = data[:4]
            value = struct.unpack('<f', bytes(part))
            results.append(value[0])
            data = data[4:]
        return results

    def usbConnect(self, vid, pid):
        # vid = 1155  # replace with the Vendor ID of the USB device
        # pid = 22336  # replace with the Product ID of the USB device
        if self._usbCtrl.serial:
            if self._usbCtrl.serial.isOpen():
                print("USB Already Opened")
                return
            else:
                usbStatus = self._usbCtrl.connectUsb(vid, pid)
                self._model.usbConnStatus = usbStatus
                print('USB connect successfully') if usbStatus else print('USB connect failed')
        else:
            usbStatus = self._usbCtrl.connectUsb(vid, pid)
            self._model.usbConnStatus = usbStatus
            print('USB connect successfully') if usbStatus else print('USB connect failed')

    def moveHome(self):
        frame = self._usbCtrl.makeFrame("HOME", "AUT", [0, 0, 0])
        print("MOVE HOME");
        print("frame", bytearray(frame))
        self._usbCtrl.sendUsb(bytearray(frame))

    def moveJoint(self, joint1Deg, joint2Deg, joint3Deg):
        # frame = self._usbCtrl.makeFrame("GJOI", "MAN", [joint1Deg, joint2Deg, joint3Deg])
        x = 260
        y = -191
        z = 120
        frame = self._usbCtrl.makeFrame("GPLA", "AUT", [x, y, z])
        print("frame", bytearray(frame))
        self._usbCtrl.sendUsb(bytearray(frame))

    def movePos(self, x, y, z=0):
        frame = self._usbCtrl.makeFrame("GPOS", "AUT", [x, y, z])
        # print("move to posistion", x, y, z)
        # print("frame", ( )
        # self._model.motorGraphCurr = [1, 2, 3]
        self._usbCtrl.sendUsb(bytearray(frame))

    def moveConveyor(self,  speed, mode , Kp=0, Ki=0, Kd=0):
        print(mode, speed)
        if(mode == "Fuzzy-PID"):
            frame = self._usbCtrl.makeFrame("SFUZ", "000", [0, 0, 0])
            print(bytearray(frame))
            self._usbCtrl.sendUsb(bytearray(frame))

            frame = self._usbCtrl.makeFrame("SVEL", "000", [0, 0, speed])
            print(bytearray(frame))
            self._usbCtrl.sendUsb(bytearray(frame))

            frame = self._usbCtrl.makeFrame("CTUN", "000", [0, 0, 0])
            print(bytearray(frame))
            self._usbCtrl.sendUsb(bytearray(frame))

        if (mode == "PID"):
            frame = self._usbCtrl.makeFrame("SPID", "000", [Kp, Ki, Kd])
            print(bytearray(frame))
            self._usbCtrl.sendUsb(bytearray(frame))

            frame = self._usbCtrl.makeFrame("SVEL","000", [0, 0, speed])
            print(bytearray(frame))
            self._usbCtrl.sendUsb(bytearray(frame))

            frame = self._usbCtrl.makeFrame("CTUN", "000", [0, 0, 0])
            print(bytearray(frame))
            self._usbCtrl.sendUsb(bytearray(frame))

    def movePosPlace(self, x, y, z):
        frame = self._usbCtrl.makeFrame("GPLA", "AUT", [x, y, z])
        # print("move to posistion", x, y, z)
        for i in frame:
            print(hex(i))
        # print("frame", ( )
        self._usbCtrl.sendUsb(bytearray(frame))

    def chosePosDependOnLabel(self, label):
        if label == "Pepsi":
            self.LabelisPepsi(label)
        elif label == "Starbucks":
            self.LabelisStarBucks(label)
        elif label == "Monsters":
            self.LabelisMonster(label)

    def LabelisPepsi(self, label):
        x = 90
        y = 140
        z = 170
        # self.View.onPickedupDetectRobot(self, x, y, z, label)
        self.movePosPlace(x, y, z)

    def LabelisStarBucks(self, label):
        x = 1
        y = 190
        z = 170
        # self.View.onPickedupDetectRobot(self, x, y, z, label)
        self.movePosPlace(x, y, z)

    def LabelisMonster(self, label):
        x = 90
        y = 240
        z = 170
        # self.View.onPickedupDetectRobot(self, x, y, z, label)
        self.movePosPlace(x, y, z)
