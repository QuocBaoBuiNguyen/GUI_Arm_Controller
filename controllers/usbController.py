import serial
import serial.tools.list_ports
from util.dataTypes import arrayFloat
import threading
import time

class UsbController(object):
    def __init__(self, f_cb):
        print("usb_controller: Init")
        self._isConnected = 0
        self.STX = 0X02
        self.ACK = 0X06
        self.SYNC = 0X16
        self.ETX = 0x03
        self.SYNC_BYTES = b'\x06\x03'
        self.FRAME_SIZE = 22
        self.serial = None
        self.readUsbCallback = f_cb

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
            self._isConnected = 1
            self.serial.readThread = threading.Thread(target=self.readUsb, args=[])
            self.serial.readThread.start()
            return self._isConnected

    def sendUsb(self, data):
        try:
            self.serial.write(data)
        except:
            print("Send Error: Check connect USB or something!!")
            return

    def readUsb(self):
        try:
            while self._isConnected:
                self.serial.reset_input_buffer()
                #self.serial.read_until(self.SYNC_BYTES)
                ser_bytes = self.serial.read(self.FRAME_SIZE)
#                print(ser_bytes)
                self.readUsbCallback(ser_bytes)
#                print(f'\r{ser_bytes}', end='', flush=True)
                time.sleep(0.25)
        finally:
            self.serial.close()

    def makeFrame(self, frameCmd, frameOpt, frameData):
        # Init
        frame = []
        datas = [arrayFloat() for i in range(0, 3)]

        # Config frame
        frame.insert(0, 0x02)
        frame[1:1] = [ord(c) for c in frameCmd]
        frame[5:5] = [ord(c) for c in frameOpt]
        # print(frameData)
        # print(len(frameData))
        for i in range(0, len(frameData)):
            datas[i].float_num = frameData[i]

        for i in range(0, len(frameData)):
            for j in range(0, 4):
                frame.append((datas[i].float_arr[j]))

        frame.insert(20, 0x16)
        frame.insert(21, 0x03)
        return frame

    def parseFrame(self, frame):
        datas = [arrayFloat() for i in range(0, 3)]
        # Parse frame
        if frame[0] == 0x02 and frame[21] == 0x03:
            cmd = frame[1:4]
            opt = frame[5:7]
            for i in range(0, 11):
                datas[i] = frame[8 + i]
            #switch case
            print(cmd)
            print(opt)
            print(datas)
        else:
            print("usbController: Frame is not correct")

