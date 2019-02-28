from panel.max7219 import Lcd
from panel.adc import Adc
from panel.ledstrip import LedStrip

class Ecam:

	def __init__(self):
		self.active = True
		self.lcd = Lcd(40000, 1)
		self.lcd.setModeAll(Lcd.NORMAL)
		self.lcd.setIntensityAll(15)
		self.lcd.setMaxDigits(0,3)
		self.lcd.setDecodeModeForDigits(0,[2])
		self.lcd.setDigitValue(0, 1, 255)
		self.brightness = 15
#		self.adc = Adc(400000)
#		self.adc.readInput(1)
		self.x = 0
		self.receiver = 0
		self.ledstrip = LedStrip()

	def startReceiver(self, hostname, hostport):
		pass

	def stopReceiver(self):
		pass

	def stop(self):
		if self.receiver != 0:
			self.receiver.stop()
		print ("...ECAM terminated...")

	def test(self):
#		self.adc.readInput(1)
#		self.adc.readInput(2)
		self.lcd.setDigitValue(0, 0, self.x)
		self.lcd.setDigitValue(0, 1, self.x)
		self.lcd.setDigitValue(0, 2, self.x)
		self.x = self.x + 1
		if self.x >255:
			self.x = 0
