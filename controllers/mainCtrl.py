import array as arr
from controllers.usbController import usbController
from util.dataType import arrayFloat

class Controller(object):
    def __init__(self):
        print("main_ctrl: Init")
        # self._model = model

        self._usbCtrl = usbController()

    def usbConnect(self, vid, pid):
        print("connecting usb")
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

    def moveCmd(self, x, y, z):

        a = []
        datas = [arrayFloat() for i in range(0,3)]

        a.insert(0, 0x02)
        a[1:1] = [ord(c) for c in "GPOS"]
        a[5:5] = [0, 0, 0]

        datas[0].float_num = x
        datas[1].float_num = y
        datas[2].float_num = z
        print(type(datas[0].float_arr))
        for i in range(0, 3):
            for j in range(0, 4):
                # print(i, j)
                a.append((datas[i].float_arr[j]))

        a.insert(20, 0x16)
        a.insert(21, 0x03)
        print("MOVE CMD")
        print(x, y, z)
        # data2 = bytearray(a)
        # print(data2)
        print(bytearray(a))
        self._usbCtrl.sendUsb(bytearray(a))
