import sys
from PyQt5.uic import loadUi
from time import time
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QGraphicsWidget
from PyQt5.QtChart   import QChart, QLineSeries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from views.robotCtrlUi import robotCtrlUi

from PyQt5 import QtGui
from PyQt5.QtGui import QImage, QPixmap

import numpy as np
import os
import math

import cv2
from PIL import Image

import torch

class CameraController(object):

    def __init__(self,  f_cb):
        print("main_view: Init")

        self.thread = {}
        self.photo_capture_callback = f_cb

    def closeEvent(self, event):
        self.stop_capture_video()

    def closeEvent(self, event):
        self.stop_capture_video()

    def stop_capture_video(self):
        self.thread[1].pause_stream()
        self.thread[1].stop()

    def start_capture_video(self):
        self.thread[1] = live_stream(index=1)
        self.thread[1].start()

        self.thread[1].signal.connect(self.show_wedcam)

    def show_wedcam(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = convert_cv_qt(cv_img)
        # self._ui.imgLabel.setPixmap(qt_img)
        # self.imgLabel.setScaledContents(True)
        self.photo_capture_callback(qt_img)

def convert_cv_qt(cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(700, 500, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)

class live_stream(QThread):
    signal = pyqtSignal(np.ndarray)

    def __init__(self, index):
        self.device = None
        self.out_file = None
        self.classes = None
        self.model = None
        self.gg = True
        self.player = None
        self.index = index
        print("start threading", self.index)
        super(live_stream, self).__init__()

    def run(self):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param out_file: A valid output file name.
        """
        self.model = self.load_model()  # load model
        self.classes = self.model.names
        self.out_file = "Labeled_Video.avi"
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.run_program()

    def get_video_from_url(self):
        """
        Creates a new video streaming object to extract video frame by frame to make prediction on.
        :return: opencv2 video capture object, with lowest quality frame available for video.
        """
        return cv2.VideoCapture(0)  # "D:/8.Record video/movie.mp4"

    def load_model(self):
        """
        Loads Yolo5 model from pytorch hub.
        :return: Trained Pytorch model.
        """
        # model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        #model = torch.hub.load('ultralytics/yolov5', 'custom', path='E:\HCMUT\FinalProject\GUI\GUI_Arm_Controller\model\YOLOv5_FlagsDetection')
        # model = torch.hub.load('yolov5-master', 'custom', path='yolov5s.pt', source='local')
        # model = torch.hub.load('ultralytics/yolov5', 'custom',
        #                        path='E:\HCMUT\FinalProject\GUI\GUI_Arm_Controller\model\YOLOv5_DrinksLogos_Segment')
        model = torch.hub.load('ultralytics/yolov5', 'custom',
                               path='E:\HCMUT\FinalProject\GUI\GUI_Arm_Controller\model\YOLOv5_DrinksLogos_V2')
        return model

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
        return labels, cord

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        hue, saturation, value = cv2.split(hsv)
        blurred_sat = cv2.GaussianBlur(saturation, (5, 5), 0)
        edges = cv2.Canny(blurred_sat, 45, 100)

        kernel = np.ones((3, 3), np.uint8)
        dilate = cv2.dilate(edges, kernel, iterations=2)
        erode = cv2.erode(dilate, kernel, iterations=2)

        contours, hierarchy = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        for contour in contours:

            area = cv2.contourArea(contour)
            if area >= 6000:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                print(box)

                labels, cord = results
                n = len(labels)
                x_shape, y_shape = frame.shape[1], frame.shape[0]
                for i in range(n):
                    row = cord[i]
                    print("ddd", round(cord[i][4], 2))
                    if row[4] >= 0.1:
                        x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                            row[3] * y_shape)
                        print("x1 = ", x1,", y1 = ", y1,", x2 = ", x2, ", y2 = ", y2)
                        print(box[3][0], box[3][1], box[1][0], box[1][1])
                        if box[3][0] >= x1 and box[3][1] >= y1 and box[1][0] <= x2 and box[1][1] <= y2:
                            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
                            bgr = (0, 250, 0)
                            cv2.putText(frame, self.class_to_label(labels[i]) + " " + str(round(row[4], 2)), (box[3][0], box[3][1]),
                                                             cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
                            radius = 2
                            #center = (int(x1 + (x2 - x1) // 2), int(y1 + (y2 - y1) // 2))
                            center = (int(box[3][0] + (box[1][0] - box[3][0]) // 2), int(box[3][1] + (box[1][1] - box[3][1]) // 2))
                            #print(self.class_to_label(labels[i]), center)
                            object_label = self.class_to_label(labels[i])
                            cv2.circle(frame, center, radius, (250, 0, 0), 2)
                            cv2.putText(frame, str(center[0]) + " " + str(center[1]), center,
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
            else:
                object_label = "No object"
                center = [0, 0]
        print("end loop")

        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        # labels, cord = results
        # n = len(labels)
        # x_shape, y_shape = frame.shape[1], frame.shape[0]
        # for i in range(n):
        #     row = cord[i]
        #     print("ddd", round(cord[i][4], 2))
        #     if row[4] >= 0.1:
        #         x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
        #             row[3] * y_shape)
        #         print(x1, y1, x2, y2)
        #
        #         bgr = (0, 250, 0)
        #         cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
        #         radius = 2
        #         center = (int(x1 + (x2 - x1) // 2), int(y1 + (y2 - y1) // 2))
        #         print(self.class_to_label(labels[i]), center)
        #         cv2.circle(frame, center, radius, bgr, 2)
        #         cv2.putText(frame, self.class_to_label(labels[i]) + " " + str(round(row[4], 2)), (x1, y1),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)
        return frame, object_label, center

    def run_program(self):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: voidv
        """
        self.player = self.get_video_from_url()
        assert self.player.isOpened()
        x_shape = int(self.player.get(cv2.CAP_PROP_FRAME_WIDTH))
        y_shape = int(self.player.get(cv2.CAP_PROP_FRAME_HEIGHT))
        four_cc = cv2.VideoWriter_fourcc(*"MJPG")
        out = cv2.VideoWriter(self.out_file, four_cc, 20, (x_shape, y_shape))

        while True:
            from controllers.mainCtrl import Controller
            os.chdir('E:\HCMUT\FinalProject\GUI\GUI_Arm_Controller\model')
            start_time = time()
            ret, frame = self.player.read()
            assert ret
            results = self.score_frame(frame)
            frame, objectLabel, center = self.plot_boxes(results, frame)
            if (center == [300, 300]) and (objectLabel != "No object"):
                self.Controller.movePos_Auto(self, objectLabel)
            print("object is " + objectLabel, center)
            cv2.imwrite('result.jpg', frame)
            end_time = time()
            fps = 1 / (np.round(end_time - start_time, 3))
            print(f"Frames Per Second : {round(fps, 2)} FPS")
            # out.write(frame)
            self.signal.emit(frame)
            if not self.gg:
                print("stop capture video")
                break

    def stop(self):
        print("stop threading", self.index)
        self.player.release()
        # cv2.destroyAllWindows()
        # self.terminate()

    def pause_stream(self):
        self.gg = False






