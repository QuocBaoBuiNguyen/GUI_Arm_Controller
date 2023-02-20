import serial
import serial.tools.list_ports
from util.dataType import arrayFloat

class UsbController(object):
    def __init__(self):
        print("usb_controller: Init")
        self.serial = None;

    def connectUsb(self, vid, pid):
        print("usb_controller: Trying to connect")
        ports = serial.tools.list_ports.comports()
        self._isConnected = 0;
        for port in ports:
            if port.vid == vid and port.pid == pid:
                device_path = port.device
            else:
                # print("Incorrect PID and VID of USB")
                continue
            self.serial = serial.Serial(device_path, baudrate=9600)
            self._isConnected = 1
        return self._isConnected

    def sendUsb(self, data):
        try:
            self.serial.write(data)
        except:
            print("Send Error: Check connect USB or something!!")
            return

    def makeFrame(self, frameCmd, framdOpt, frameData):
        # Init
        frame = []
        datas = [arrayFloat() for i in range(0, 3)]

        # Config frame
        frame.insert(0, 0x02)
        frame[1:1] = [ord(c) for c in frameCmd]
        frame[5:5] = framdOpt
        print(frameData)
        print(len(frameData))
        for i in range(0, len(frameData)):
            datas[i].float_num = frameData[i]

        for i in range(0, len(frameData)):
            for j in range(0, 4):
                frame.append((datas[i].float_arr[j]))

        frame.insert(20, 0x16)
        frame.insert(21, 0x03)
        return frame
