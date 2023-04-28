import RPi.GPIO as GPIO
import time
import subprocess

script_path = 'cam.py'
ul_path = 'ul.py'
sensor = 16
buzzer = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)

GPIO.output(buzzer,False)
print("IR Sensor Ready.....")
print( " ")

try: 
   while True:
      if GPIO.input(sensor):
          #GPIO.output(buzzer,True)
          print("Yet to sense object...")
          while GPIO.input(sensor):
              time.sleep(0.2)
      else:
          #GPIO.output(buzzer,False)
          print("Object Detected")
          process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          process = subprocess.Popen(['python', ul_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

except KeyboardInterrupt:
    GPIO.cleanup()
