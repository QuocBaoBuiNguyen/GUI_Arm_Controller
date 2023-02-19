import serial
from controllers.usbController import usbController

class Controller(object):
    def __init__(self, model):
        print("main_ctrl: Init")
        self._model = model

        self._usbCtrl = usbController()

    def usbConnect(self, vid, pid):
        print("connecting usb")
        print(pid, vid)
        # vid = 1155  # replace with the Vendor ID of the USB device
        # pid = 22336  # replace with the Product ID of the USB device
        if self._usbCtrl.serial:
            if self._usbCtrl.serial.isOpen():
                print("USB Already Opened")
                return
            else:
                print("connecting usb")
                self._usbCtrl.connectUsb(vid, pid);
        else:
            self._usbCtrl.connectUsb(vid, pid);

    def moveHome(self):
        print("MOVE HOME");

    def moveCmd(self):
        print("MOVE CMD");


