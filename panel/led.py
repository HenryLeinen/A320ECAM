from panel.max7219 import Lcd

# This class interacts with the LED Driver IC MAX7219 in order to drive an LED matrix of size ROWS x COLUMNS
# To light only one LED, call the 'activateLED' member and pass a tuple or array giving the row and the column
# index for the particular led to be lit. Both indices are zero based, the column shall be given as bitmask (i.e. 2^column value)

class Leds:

	def __init__(self, rows, columns):
		self.lcd = Lcd(40000,1)
		self.lcd.setModeAll(Lcd.NORMAL)
		self.lcd.setIntensityAll(5)
		self.lcd.setMaxDigits(0,rows)
		self.lcd.setDecodeModeForDigits(0,[])
		for r in range(0,rows):
			self.lcd.setDigitValue(0,r,0)
		self.lcd.flush(0)
		self.Brightness = 15
		self.rows = rows
		self.cols = columns

	def activateLED(self, led):
		self.activateLEDs([led])

	def activateLEDs(self, leds):
		row = [0 for r in range(self.rows)]
		for l in leds:
			row[l[0]] = row[l[0]] + l[1]
		for r in range(self.rows):
			self.lcd.setDigitValue(0,r,row[r])
		self.lcd.flush(0)

	def setBrightness(self, b):
		self.Brightness = b
		self.lcd.setIntensityAll(0,b)

