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
            print(port.vid, port.pid)
            if port.vid == vid and port.pid == pid:
                device_path = port.device
            else:
                print("Incorrect PID and VID of USB")
                continue
            self.serial = serial.Serial(device_path, baudrate=9600)

    def sendUsb(self, data):
        self.serial.send(data)