import array as arr
from controllers.usbController import UsbController
# from controllers.cameraController import CameraController
from util.dataTypes import arrayFloat
import struct

class Controller(object):
    def __init__(self, model):
        print("main_ctrl: Init")
        self._model = model
        self._usbCtrl = UsbController(self.receiveUsbEventHandler)
        #self._cameraCtrl = CameraController(self.photoCaptureEventCb)

    def photoCaptureEventCb(self, imagePath):
        self._model.cameraCurrImg = imagePath

    def startDetectionTimer(self):
        self._cameraCtrl.startTimer()

    def endDetectionTimer(self):
        self._cameraCtrl.endTimer()

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
                    print(joint_angle1, joint_angle2, joint_angle3 )

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
        frame = self._usbCtrl.makeFrame("HOME", [0, 0, 0], [0, 0, 0])
        print("MOVE HOME");
        print("frame", bytearray(frame))
        self._usbCtrl.sendUsb(bytearray(frame))

    def moveJoint(self, joint1Deg, joint2Deg, joint3Deg):
        frame = self._usbCtrl.makeFrame("GJOI", [0, 0, 0], [joint1Deg, joint2Deg, joint3Deg])
        print("frame", bytearray(frame))
        self._usbCtrl.sendUsb(bytearray(frame))

    def movePos(self, x, y, z):
        frame = self._usbCtrl.makeFrame("GPOS", [0, 0, 0], [x, y, z])
        # print("move to posistion", x, y, z)
        for i in frame:
            print(hex(i))
        # print("frame", ( )
        self._usbCtrl.sendUsb(bytearray(frame))
