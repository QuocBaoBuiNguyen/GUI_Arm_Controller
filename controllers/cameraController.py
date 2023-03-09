# import numpy as np
# import os
#
# from tflite_model_maker.config import ExportFormat
# from tflite_model_maker import model_spec
# from tflite_model_maker import object_detector
#
# import tensorflow as tf
#
# from PyQt5.QtCore import *
#
# assert tf.__version__.startswith('2')
# print(tf. __version__)
#
# tf.get_logger().setLevel('ERROR')
# from absl import logging
# logging.set_verbosity(logging.ERROR)
#
# spec = model_spec.get('efficientdet_lite2')
#
# import cv2
# import time
# from PIL import Image
#
# class CameraController(object):
#     def __init__(self, f_cb):
#         start_time = time.time()
#         os.chdir('D:/NCKH/AppQt/Project/ArmGUI/model')
#         interpreter = tf.lite.Interpreter(model_path="EfficientDet2_Flags.tflite")
#         interpreter.allocate_tensors()
#         input_details = interpreter.get_input_details()
#         output_details = interpreter.get_output_details()
#
#         model_path = 'EfficientDet2_Flags.tflite'
#
#         self.classes = ['Vietnam', 'USA', 'Germany', 'Belgium']
#
#         # Define a list of colors for visualization
#         self.COLORS = np.random.randint(0, 255, size=(len(self.classes), 3), dtype=np.uint8)
#
#         self.timer = QTimer()
#         self.timer.timeout.connect(lambda: self.start_detect())
#         self.photo_capture_callback = f_cb
#
#     def preprocess_image(self, image_path, input_size):
#         """Preprocess the input image to feed to the TFLite model"""
#         img = tf.io.read_file(image_path)
#         img = tf.io.decode_image(img, channels=3)
#         img = tf.image.convert_image_dtype(img, tf.uint8)
#         original_image = img
#         resized_img = tf.image.resize(img, input_size)
#         resized_img = resized_img[tf.newaxis, :]
#         resized_img = tf.cast(resized_img, dtype=tf.uint8)
#         return resized_img, original_image
#
#     def set_input_tensor(self, interpreter, image):
#         """Set the input tensor."""
#         tensor_index = interpreter.get_input_details()[0]['index']
#         input_tensor = interpreter.tensor(tensor_index)()[0]
#         input_tensor[:, :] = image
#
#     def get_output_tensor(self, interpreter, index):
#         """Retur the output tensor at the given index."""
#         output_details = interpreter.get_output_details()[index]
#         tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
#         return tensor
#
#     def detect_objects(self, interpreter, image, threshold):
#         """Returns a list of detection results, each a dictionary of object info."""
#         # Feed the input image to the model
#         # self.set_input_tensor(interpreter, image)
#         # interpreter.invoke()
#
#         signature_fn = interpreter.get_signature_runner()
#
#         output = signature_fn(images = image)
#
#         count = int(np.squeeze(output['output_0']))
#         scores = np.squeeze(output['output_1'])
#         classes = np.squeeze(output['output_2'])
#         boxes = np.squeeze(output['output_3'])
#
#         # # Get all outputs from the model
#         # scores = self.get_output_tensor(interpreter, 0)
#         # boxes = self.get_output_tensor(interpreter, 1)
#         # count = int(self.get_output_tensor(interpreter, 2))
#         # classes = self.get_output_tensor(interpreter, 3)
#
#         results = []
#         for i in range(count):
#             if scores[i] >= threshold:
#                 result = {
#                     'bounding_box': boxes[i],
#                     'class_id': classes[i],
#                     'score': scores[i]
#                 }
#                 results.append(result)
#         return results
#
#     def run_odt_and_draw_results(self, image_path, interpreter, threshold=0.5):
#         """Run object detection on the input image and draw the detection results"""
#         # Load the input shape required by the model
#         _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']
#
#         # Load the input image and preprocess it
#         preprocessed_image, original_image = self.preprocess_image(
#             image_path,
#             (input_height, input_width)
#         )
#
#         # Run object detection on the input image
#         results = self.detect_objects(interpreter, preprocessed_image, threshold=threshold)
#         print(results)
#         # Plot the detection results on the input image
#         original_image_np = original_image.numpy().astype(np.uint8)
#         for obj in results:
#             # skip noise bounding box
#             if obj['score'] < 0.8:
#                 continue
#             # Convert the object bounding box from relative coordinates to absolute
#             # coordinates based on the original image resolution
#             ymin, xmin, ymax, xmax = obj['bounding_box']
#             xmin = int(xmin * original_image_np.shape[1])
#             xmax = int(xmax * original_image_np.shape[1])
#             ymin = int(ymin * original_image_np.shape[0])
#             ymax = int(ymax * original_image_np.shape[0])
#
#             # Find the class index of the current object
#             class_id = int(obj['class_id'])
#
#             # Draw the bounding box and label on the image
#             color = [int(c) for c in self.COLORS[class_id]]
#             cv2.rectangle(original_image_np, (xmin, ymin), (xmax, ymax), color, 2)
#
#             # Draw the center of bounding box
#             center = (int(xmin + (xmax - xmin) // 2), int(ymin + (ymax - ymin) // 2))
#             print(class_id, center)
#             radius = 2
#             cv2.circle(original_image_np, center, radius, color, 2)
#
#             # Make adjustments to make the label visible for all objects
#             y = ymin - 15 if ymin - 15 > 15 else ymin + 15
#             label = "{}: {:.0f}%".format(self.classes[class_id], obj['score'] * 100)
#             cv2.putText(original_image_np, label, (xmin, y),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#
#         # Return the final image
#         original_uint8 = original_image_np.astype(np.uint8)
#         return original_uint8
#
#     def photo_capture(self):
#         vid = cv2.VideoCapture(1)  # 0 for laptop webcam, 1 for logi webcam
#         ret, frame = vid.read()
#         #print(ret)
#         #print(frame)
#         cv2.imwrite('webcam.jpg', frame)
#         # vid.release()
#
#         # Run object detection and show the detection results
#
#         # define a video capture object
#         # vid = cv2.VideoCapture(0)
#
#     def startTimer(self):
#         self.timer.start(10)
#
#     def endTimer(self):
#         self.timer.stop()
#
#     def start_detect(self):
#
#         interpreter = tf.lite.Interpreter(model_path='EfficientDet2_Flags.tflite')
#         interpreter.allocate_tensors()
#
#         INPUT_IMAGE_URL = "D:/NCKH/AppQt/Project/ArmGUI/model/webcam.jpg"
#         DETECTION_THRESHOLD = 0.5
#
#         os.chdir('D:/NCKH/AppQt/Project/ArmGUI/model')
#         self.photo_capture()
#
#         # INPUT_IMAGE_URL = "E:/HCMUT/FinalProject/FinalProject/webcamphoto/webcam.jpg"
#         # DETECTION_THRESHOLD = 0.5
#
#         # Load the TFLite model
#         # %cd /content/gdrive/MyDrive/EfficientNet/trainedmodel
#         # interpreter = tf.lite.Interpreter(model_path='EfficientDet2_Flags.tflite')
#         # interpreter.allocate_tensors()
#
#         # Run inference and draw detection result on the local copy of the original file
#         detection_result_image = self.run_odt_and_draw_results(
#             INPUT_IMAGE_URL,
#             interpreter,
#             threshold=DETECTION_THRESHOLD
#         )
#         # imgresized = cv2.resize(detection_result_image, (1000, 1000))
#         # imgresized = cv2.cvtColor(imgresized, cv2.COLOR_RGB2BGR)
#         # cv2.imshow('', imgresized)
#         im = cv2.cvtColor(detection_result_image, cv2.COLOR_RGB2BGR)
#         cv2.imwrite('result.jpg', im)
#         print()
#         self.photo_capture_callback('result.jpg')
#
#
#
#
