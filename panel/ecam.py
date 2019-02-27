from panel.max7219 import Lcd



class Ecam:

	def __init__(self):
		self.active = True
		self.lcd = Lcd(400000, 1)
		self.lcd.setModeAll(Lcd.NORMAL)
		self.lcd.setIntensityAll(15)
		self.lcd.setMaxDigits(0,7)
		self.lcd.setDecodeModeForDigits(0,[0])
		self.brightness = 15

	def startReceiver(self, hostname, hostport):
		pass

	def stopReceiver(self):
		pass

	def stop(self):
		if self.receiver != 0:
			self.receiver.stop()
		print ("...ECAM terminated...")
