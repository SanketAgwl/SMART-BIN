#!/usr/bin/python
# import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import credentials, db

length= 100

cred = credentials.Certificate("service.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://waste-management-74338-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('/Bin')
ref.set({'id': '1', 'status': 'on', 'level': '0'})

try:
      GPIO.setmode(GPIO.BOARD)

      PIN_TRIGGER = 13
      PIN_ECHO = 15

      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN_ECHO, GPIO.IN)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      print ("Waiting for sensor to settle")

      time.sleep(2)

      print( "Calculating distance")

      GPIO.output(PIN_TRIGGER, GPIO.HIGH)

      time.sleep(0.00001)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)
      pulse_start_time = 0
      pulse_end_time = 0
      while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
      while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

      pulse_duration = pulse_end_time - pulse_start_time
      distance = round(pulse_duration * 17150, 2)
      print ("Distance:",distance,"cm")
      level = (length - distance) * 100 / length
      ref.update({'id': '1', 'status': 'on', 'level': level})

finally:
      GPIO.cleanup()
