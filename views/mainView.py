import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QGraphicsWidget
from PyQt5.QtChart   import QChart, QLineSeries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from views.robotCtrlUi import robotCtrlUi

print("START")
from PyQt5.QtGui import QImage, QPixmap

import numpy as np
import os

from tflite_model_maker.config import ExportFormat
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

import tensorflow as tf
assert tf.__version__.startswith('2')
print(tf. __version__)

#print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)

spec = model_spec.get('efficientdet_lite2')

import cv2
from PIL import Image

#class View(QWidget):
class View(QMainWindow):

    def __init__(self,  controller):
        print("main_view: Init")
        super(View, self).__init__()

        self._ui = loadUi("resources/main.ui", self)

        self._controller = controller
        self._robotCtrlUi = robotCtrlUi(self._ui)

        os.chdir('E:\HCMUT\FinalProject\GUI\GUI_Arm_Controller\model')
        interpreter = tf.lite.Interpreter(model_path="EfficientDet2_Flags.tflite")
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        model_path = 'EfficientDet2_Flags.tflite'

        self.classes = ['Vietnam', 'USA', 'Germany', 'Belgium']

        # Define a list of colors for visualization
        self.COLORS = np.random.randint(0, 255, size=(len(self.classes), 3), dtype=np.uint8)

        # self.connectBtn.clicked.connect(lambda: self._controller.usbConnect(int(self._ui.vidTxt.toPlainText()),
        #                                                                     int(self._ui.pidTxt.toPlainText())))
        self.connectBtn.clicked.connect(lambda: self._controller.usbConnect(1155, 22336))
        self.DetectButton.clicked.connect(self.detect_object)

        self._ui.movCmdBtn.clicked.connect(self.getPosistion)

    def getPosistion(self):
        # if str(self._ui.x_txt.toPlainText()) != "" and str(self._ui.y_txt.toPlainText()) != "" and str(self._ui.z_txt.toPlainText()) != "":
            self._controller.moveCmd(float(self._ui.x_txt.toPlainText()),
                                     float(self._ui.y_txt.toPlainText()),
                                     float(self._ui.z_txt.toPlainText()))
        # else:
        #     print("At least one field of coordinate posistion is empty")

    def preprocess_image(self, image_path, input_size):
        """Preprocess the input image to feed to the TFLite model"""
        img = tf.io.read_file(image_path)
        img = tf.io.decode_image(img, channels = 3)
        img = tf.image.convert_image_dtype(img, tf.uint8)
        original_image = img
        resized_img = tf.image.resize(img, input_size)
        resized_img = resized_img[tf.newaxis, :]
        return resized_img, original_image

    def set_input_tensor(self, interpreter, image):
        """Set the input tensor."""
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def get_output_tensor(self, interpreter, index):
        """Retur the output tensor at the given index."""
        output_details = interpreter.get_output_details()[index]
        tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
        return tensor

    def detect_objects(self, interpreter, image, threshold):
        """Returns a list of detection results, each a dictionary of object info."""
        # Feed the input image to the model
        self.set_input_tensor(interpreter, image)
        interpreter.invoke()

        # Get all outputs from the model
        scores = self.get_output_tensor(interpreter, 0)
        boxes = self.get_output_tensor(interpreter, 1)
        count = int(self.get_output_tensor(interpreter, 2))
        classes = self.get_output_tensor(interpreter, 3)

        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                    'bounding_box': boxes[i],
                    'class_id': classes[i],
                    'score': scores[i]
                }
                results.append(result)
        return results

    def run_odt_and_draw_results(self, image_path, interpreter, threshold=0.5):
        """Run object detection on the input image and draw the detection results"""
        # Load the input shape required by the model
        _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']

        # Load the input image and preprocess it
        preprocessed_image, original_image = self.preprocess_image(
            image_path,
            (input_height, input_width)
        )

        # Run object detection on the input image
        results = self.detect_objects(interpreter, preprocessed_image, threshold=threshold)
        print(results)
        # Plot the detection results on the input image
        original_image_np = original_image.numpy().astype(np.uint8)
        for obj in results:
            # skip noise bounding box
            if obj['score'] < 0.8:
                continue
            # Convert the object bounding box from relative coordinates to absolute
            # coordinates based on the original image resolution
            ymin, xmin, ymax, xmax = obj['bounding_box']
            xmin = int(xmin * original_image_np.shape[1])
            xmax = int(xmax * original_image_np.shape[1])
            ymin = int(ymin * original_image_np.shape[0])
            ymax = int(ymax * original_image_np.shape[0])

            # Find the class index of the current object
            class_id = int(obj['class_id'])

            # Draw the bounding box and label on the image
            color = [int(c) for c in self.COLORS[class_id]]
            cv2.rectangle(original_image_np, (xmin, ymin), (xmax, ymax), color, 2)

            # Draw the center of bounding box
            center = (int(xmin + (xmax - xmin) // 2), int(ymin + (ymax - ymin) // 2))
            print(class_id, center)
            radius = 2
            cv2.circle(original_image_np, center, radius, color, 2)

            # Make adjustments to make the label visible for all objects
            y = ymin - 15 if ymin - 15 > 15 else ymin + 15
            label = "{}: {:.0f}%".format(self.classes[class_id], obj['score'] * 100)
            cv2.putText(original_image_np, label, (xmin, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Return the final image
        original_uint8 = original_image_np.astype(np.uint8)
        return original_uint8

    def photo_capture(self):
        vid = cv2.VideoCapture(1)  # 0 for laptop webcam, 1 for logi webcam
        ret, frame = vid.read()
        print(ret)
        print(frame)
        cv2.imwrite('webcam.jpg', frame)
        # vid.release()

        # Run object detection and show the detection results

        # define a video capture object
        # vid = cv2.VideoCapture(0)

    def detect_object(self):

        interpreter = tf.lite.Interpreter(model_path='EfficientDet2_Flags.tflite')
        interpreter.allocate_tensors()

        INPUT_IMAGE_URL = "E:/HCMUT/FinalProject/FinalProject/webcamphoto/webcam.jpg"
        DETECTION_THRESHOLD = 0.5

    #while (True):

        os.chdir('E:/HCMUT/FinalProject/FinalProject/webcamphoto')
        self.photo_capture()

        # INPUT_IMAGE_URL = "E:/HCMUT/FinalProject/FinalProject/webcamphoto/webcam.jpg"
        # DETECTION_THRESHOLD = 0.5

        # Load the TFLite model
        # %cd /content/gdrive/MyDrive/EfficientNet/trainedmodel
        # interpreter = tf.lite.Interpreter(model_path='EfficientDet2_Flags.tflite')
        # interpreter.allocate_tensors()

        # Run inference and draw detection result on the local copy of the original file
        detection_result_image = self.run_odt_and_draw_results(
            INPUT_IMAGE_URL,
            interpreter,
            threshold=DETECTION_THRESHOLD
        )
        # imgresized = cv2.resize(detection_result_image, (1000, 1000))
        # imgresized = cv2.cvtColor(imgresized, cv2.COLOR_RGB2BGR)
        # cv2.imshow('', imgresized)
        im = cv2.cvtColor(detection_result_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite('result.jpg', im)

        self.imgLabel.setPixmap(QPixmap('result.jpg'))
        self.imgLabel.setScaledContents(True)
