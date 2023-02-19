# Modified by Augmented Startups & Geeky Bee
# October 2020
# Facial Recognition Attendence GUI
# Full Course - https://augmentedstartups.info/yolov4release
# *-
import sys
from PyQt5.QtWidgets import QApplication
from model.models import Model
from controllers.mainCtrl import Controller
from views.mainView import View

class App(object):
    def __init__(self):
        self.model = Model()
        self.controller = Controller(self.model)
        self.view = View(self.controller, self.model)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = App()
    ui.view.show()
    sys.exit(app.exec_())
