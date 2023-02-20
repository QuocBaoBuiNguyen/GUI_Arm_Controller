import array as arr
from controllers.usbController import UsbController
from util.dataType import arrayFloat

class Controller(object):
    def __init__(self, model):
        print("main_ctrl: Init")
        self._model = model
        self._usbCtrl = UsbController()

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
        frame = self._usbCtrl.makeFrame("GJOI", [0, 0, 0], [0, 0, 0])
        print("MOVE HOME");
        print("frame", bytearray(frame))
        self._usbCtrl.sendUsb(bytearray(frame))

    def moveJoint(self, joint1Deg, joint2Deg, joint3Deg):
        frame = self._usbCtrl.makeFrame("GJOI", [0, 0, 0], [joint1Deg, joint2Deg, joint3Deg])
        print("frame", bytearray(frame))
        self._usbCtrl.sendUsb(bytearray(frame))

    def movePos(self, x, y, z):
        frame = self._usbCtrl.makeFrame("GPOS", [0, 0, 0], [x, y, z])
        print("move to posistion", x, y, z)
        print("frame", bytearray(frame))
        self._usbCtrl.sendUsb(bytearray(frame))
