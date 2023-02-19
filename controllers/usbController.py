import serial
import serial.tools.list_ports


class usbController(object):
    def __init__(self):
        print("usb_controller: Init")
        self.serial = None;

    def connectUsb(self, vid, pid):
        print("usb_controller: Trying to connect")
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.vid == vid and port.pid == pid:
                device_path = port.device
            else:
                # print("Incorrect PID and VID of USB")
                continue
            self.serial = serial.Serial(device_path, baudrate=9600)
            print('USB connect successfully')

    def sendUsb(self, data):
        print(self.serial)
        try:
            self.serial.write(data)
        except:
            print("deo gui duoc")
            return