import RPi.GPIO as GPIO


class LedStrip:

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(18, GPIO.OUT)
		GPIO.setup(12, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)

		self.pwm_red = GPIO.PWM(18, 200)
		self.pwm_green = GPIO.PWM(12, 200)
		self.pwm_blue = GPIO.PWM(13, 200)

		self.pwm_red.start(0)
		self.pwm_green.start(5)
		self.pwm_blue.start(100)

