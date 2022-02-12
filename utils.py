# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility functions to display the pose detection results."""

from typing import List

import cv2
import numpy as np
from object_detector import Detection

# Import Servo class and the time library
from servo import Servo
import time

# Set up the servo motor
pan_servo = Servo(11, 50)
pan_servo.start()
pan_servo.set_angle(90)

# For storing the current position
pan_angle = 90
# Threshold for moving the servo
x_move_threshold = 50

# Function for moving the servo
def move(vector):
  global pan_angle, pan_servo
  if abs(vector[0]) > x_move_threshold:
    if vector[0] < 0:# object is on the right of the screen
      pan_angle += 5# move the camera in the anticlockwise direction, i.e. increase the servo angle
    else:# object is on the left of the screen
      pan_angle -= 5# move the camera in the clockwise direction, i.e. reduce the servo angle
    # Make sure that the angle is within 0 to 180
    if pan_angle < 0:
      pan_angle = 0
    if pan_angle > 180:
      pan_angle = 180
    print(pan_angle)
    pan_servo.set_angle(pan_angle)
    # The servo needs some time to move
    time.sleep(1)
  # The tilt angle can be set in the same way with vector[1]


_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 0, 255)  # red


def visualize(
    image: np.ndarray,
    detections: List[Detection],
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.

  Args:
    image: The input RGB image.
    detections: The list of all "Detection" entities to be visualize.

  Returns:
    Image with bounding boxes.
  """
  for detection in detections:
    # Draw bounding_box
    start_point = detection.bounding_box.left, detection.bounding_box.top
    end_point = detection.bounding_box.right, detection.bounding_box.bottom
    cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

    # Draw label and score
    category = detection.categories[0]
    class_name = category.label
    probability = round(category.score, 2)
    result_text = class_name + ' (' + str(probability) + ')'
    text_location = (_MARGIN + detection.bounding_box.left,
                     _MARGIN + _ROW_SIZE + detection.bounding_box.top)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)
    #Move the servo if x is detected with 50% of certainty
    if (class_name == 'bottle' and probability > 0.5):
      # Calculate the vector from the bounding box centre to the image centre
      image_centre = (image.shape[1]/2, image.shape[0]/2)
      # Bounding box attributes
      xmin, xmax, ymin, ymax = detection.bounding_box.left, detection.bounding_box.right, detection.bounding_box.top, detection.bounding_box.bottom
      bounding_box_centre = ((xmin+xmax)/2, (ymin+ymax)/2)
      vector = np.array(image_centre) - np.array(bounding_box_centre)
      # For debugging
      # cv2.circle(image, np.array(image_centre).astype(int), 2, (255, 0, 0), 3)
      # cv2.line(image, np.array(bounding_box_centre).astype(int), np.array(image_centre).astype(int), (255, 0, 0), 10)
      # With the vector, move the servo with the `move` function
      move(vector)


  return image
