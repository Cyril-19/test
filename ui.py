import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import io


def deskew(image):
    osd_data = pytesseract.image_to_osd(image)
    angle = int(re.search(r'Rotate: (\d+)', osd_data).group(1))
    if angle != 0:
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        abs_cos = abs(np.cos(np.radians(angle)))
        abs_sin = abs(np.sin(np.radians(angle)))
        bound_w = int(h * abs_sin + w * abs_cos)
        bound_h = int(h * abs_cos + w * abs_sin)
        M = cv2.getRotationMatrix2D(center, -angle, 1.0)
        M[0, 2] += bound_w / 2 - center[0]
        M[1, 2] += bound_h / 2 - center[1]
        rotated = cv2.warpAffine(image, M, (bound_w, bound_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated
    else:
       return image 


def set_image_dpi(image, dpi=300):
  height, width = image.shape[:2]
  new_width = int(width * dpi / 72)
  new_height = int(height * dpi / 72)
  resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
  return resized_image


def enhance_image(image):
    
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
    skew = deskew(image)
    image = cv2.cvtColor(skew, cv2.COLOR_BGRA2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations = 1)
    denoised = cv2.fastNlMeansDenoising(erosion, None, 30, 7, 21)
    return denoised

def extract_text(image):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    return text

def capture_image(camera_window):
  cap = cv2.VideoCapture(0)
  if not cap.isOpened():
    print("Error opening camera")
    return None
  if st.button("Start Camera"):
    while True:
      ret, frame = cap.read()
      if ret:
        camera_window.image(frame)
      else:
        break
  if st.button("Capture Image"):
    ret, frame = cap.read()
    cap.release()
    return frame


