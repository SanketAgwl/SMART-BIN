# from picamera import PiCamera
# import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials, db
import time
cred = credentials.Certificate("service.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://waste-management-74338-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('/Bin/lastImage')
import sys
import cv2
import numpy as np
import shutil
import subprocess
ledPIN = 12
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(ledPIN, GPIO.OUT, initial=GPIO.LOW)

from time import sleep
import subprocess
import datetime
import base64
from io import BytesIO
import requests

# Define the URL of the Image Processing Server
url = 'http://localhost:4544//process_image'


dt = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
dateStr,timeStr = dt.split()

def captureImage():
  stream = BytesIO()
  # camera = PiCamera()
  # camera.start_preview()
  # print("Capturing image")
  # sleep(5)
  # camera.capture(stream, format='jpeg')
  # stream.seek(0)
  # image_data = base64.b64encode(stream.getvalue()).decode('utf-8')
  # print("Image capture done")
  # camera.stop_preview()

  category = 'food'
  api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
  response = requests.get(api_url, headers={'X-Api-Key': 'hUyelggFz5ugUrE4dovkyA==iHbKoTtcg2s0qGCD', 'Accept': 'image/jpg'}, stream=True)
  image_data= response.content

  image_array = np.asarray(bytearray(image_data), dtype=np.uint8)
  image_cv2 = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
  cv2.imshow("Trash", image_cv2)
  cv2.waitKey(0)
  image_data = base64.b64encode(image_data).decode('utf-8')

  payload = {'image': image_data}
  resp = requests.post(url, json=payload)
  ref.set(image_data)
  print(resp.content)
  return resp

def respond(l):
    if (l == "1"):
      GPIO.output(ledPIN, 1)
      time.sleep(0.5)
      GPIO.output(ledPIN, 0)
    else:
      GPIO.output(ledPIN, 1)
      time.sleep(0.5)
      GPIO.output(ledPIN, 0)
      time.sleep(0.5)
      GPIO.output(ledPIN, 1)
      time.sleep(0.5)
      GPIO.output(ledPIN, 0)


seg = captureImage()
# respond(seg)