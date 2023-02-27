from PyQt5.QtCore import QObject, pyqtSignal

class Model(QObject):

    usbInfoChanged = pyqtSignal(bool)
    cameraDetectImgChanged = pyqtSignal(object)

    def __init__(self):
        super(Model, self).__init__()
        print("model: Init")

    @property
    def usbConnStatus(self):
        return self._usbConnectionStatus
    @usbConnStatus.setter
    def usbConnStatus(self, value):
        self._usbConnectionStatus = value
        self.usbInfoChanged.emit(self._usbConnectionStatus)

    @property
    def cameraCurrImg(self):
        return self._cameraCurrImg
    @cameraCurrImg.setter
    def cameraCurrImg(self, imgPath):
        self._cameraCurrImg = imgPath
        self.cameraDetectImgChanged.emit(self._cameraCurrImg)



