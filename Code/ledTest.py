import RPi.GPIO as GPIO
import time

pin = 7

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.HIGH)

setup()
while True:
	GPIO.output(pin, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(pin, GPIO.LOW)
	time.sleep(1)
