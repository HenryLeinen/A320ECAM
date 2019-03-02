from panel.adc import Adc
from panel.ledstrip import LedStrip
from panel.keymatrix import Keyboard
from panel.led import Leds

class Ecam:
	MODE_ENG 	= 1
	MODE_APU 	= 2
	MODE_BLEED 	= 3
	MODE_COND	= 4
	MODE_PRESS	= 5
	MODE_DOOR	= 6
	MODE_ELEC	= 7
	MODE_WHEEL	= 8
	MODE_HYD	= 9
	MODE_FCTL	= 10

	MODE_FUEL	= 11

	MODE_STATUS	= 20

	def __init__(self):
		self.active = True
		self.leds = Leds()
		self.adc = Adc(100000)
		self.adc.readInput(1)
		self.receiver = 0
		# Initialize the backlighting LED Strip
		self.ledstrip = LedStrip()
		# Initialize the Keyboard
		self.keys = Keyboard([2,3,4],[17,27,22,23,24,25])
		self.keys.registerCallbacks(self.onKeyPressed, 0)
		self.keys.start()
		self.mode = Ecam.MODE_STATUS

	def onKeyPressed(self, key):
		if key == Keyboard.BTN_ENG:
			print ("BTN_ENG pressed")
			self.mode = Ecam.MODE_ENG
		elif key == Keyboard.BTN_APU:
			print ("BTN_API pressed")
			self.mode = Ecam.MODE_APU
		elif key == Keyboard.BTN_BLEED:
			print ("BTN_BLEED pressed")
			self.mode = Ecam.MODE_BLEED
		elif key == Keyboard.BTN_COND:
			print ("BTN_COND pressed")
			self.mode = Ecam.MODE_COND
		elif key == Keyboard.BTN_PRESS:
			print ("BTN_PRESS pressed")
			self.mode = Ecam.MODE_PRESS
		elif key == Keyboard.BTN_DOOR:
			print ("BTN_DOOR pressed")
			self.mode = Ecam.MODE_DOOR
		elif key == Keyboard.BTN_ELEC:
			print ("BTN_ELEC pressed")
			self.mode = Ecam.MODE_ELEC
		elif key == Keyboard.BTN_WHEEL:
			print ("BTN_WHEEL pressed")
			self.mode = Ecam.MODE_WHEEL
		elif key == Keyboard.BTN_HYD:
			print ("BTN_HYD pressed")
			self.mode = Ecam.MODE_HYD
		elif key == Keyboard.BTN_FCTL:
			print ("BTN_FCTL pressed")
			self.mode = Ecam.MODE_FCTL
		elif key == Keyboard.BTN_FUEL:
			print ("BTN_FUEL pressed")
			self.mode = Ecam.MODE_FUEL
		elif key == Keyboard.BTN_STS:
			print ("BTN_STATUS pressed")
			self.mode = Ecam.MODE_STATUS
		self.updateStatus()

	def updateStatus(self):
		if self.mode == Ecam.MODE_ENG:
			print ("Mode MODE_ENG activated")
			self.leds.activateLED(Leds.LED_ENG)
		elif self.mode == Ecam.MODE_APU:
			print ("Mode MODE_APU activated")
			self.leds.activateLED(Leds.LED_APU)
		elif self.mode == Ecam.MODE_BLEED:
			print ("Mode MODE_BLEED activated")
			self.leds.activateLED(Leds.LED_BLEED)
		elif self.mode == Ecam.MODE_COND:
			print ("Mode MODE_CON activated")
			self.leds.activateLED(Leds.LED_COND)
		elif self.mode == Ecam.MODE_PRESS:
			print ("Mode MODE_PRESS activated")
			self.leds.activateLED(Leds.LED_PRESS)
		elif self.mode == Ecam.MODE_DOOR:
			print ("Mode MODE_DOOR activated")
			self.leds.activateLED(Leds.LED_DOOR)
		elif self.mode == Ecam.MODE_ELEC:
			print ("Mode MODE_ELEC activated")
			self.leds.activateLED(Leds.LED_ELEC)
		elif self.mode == Ecam.MODE_WHEEL:
			print ("Mode MODE_WHEEL activated")
			self.leds.activateLED(Leds.LED_WHEEL)
		elif self.mode == Ecam.MODE_HYD:
			print ("Mode MODE_HYD acticated")
			self.leds.activateLED(Leds.LED_HYD)
		elif self.mode == Ecam.MODE_FCTL:
			print ("Mode MODE_FCTL activated")
			self.leds.activateLED(Leds.LED_FCTL)
		elif self.mode == Ecam.MODE_FUEL:
			print ("Mode MODE_FUEL activated")
			self.leds.activateLED(Leds.LED_FUEL)
		elif self.mode == Ecam.MODE_STATUS:
			print ("Mode MODE_STATUS activated")
			self.leds.activateLED(Leds.LED_STS)

	def startReceiver(self, hostname, hostport):
		pass

	def stopReceiver(self):
		pass

	def stop(self):
		self.keys.stop()
		if self.receiver != 0:
			self.receiver.stop()
		print ("...ECAM terminated...")

	def test(self):
		pass
		self.adc.readInput(1)
		self.adc.readInput(2)
