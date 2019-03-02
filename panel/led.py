from panel.max7219 import Lcd


class Leds:

	LED_ENG		= [2,2]
	LED_BLEED	= [2,4]
	LED_PRESS	= [2,8]
	LED_ELEC	= [2,16]
	LED_HYD		= [2,32]
	LED_FUEL	= [2,64]

	LED_ALL		= [0,2]
	LED_FCTL	= [0,4]
	LED_WHEEL	= [0,8]
	LED_DOOR	= [0,16]
	LED_COND	= [0,32]
	LED_APU		= [0,64]

	LED_EMER_CANC	= [1,2]
	LED_CLR_R	= [1,4]
	LED_RCL		= [1,8]
	LED_STS		= [1,16]
	LED_CLR_L	= [1,32]
	LED_TOCONF	= [1,64]

	def __init__(self):
		self.lcd = Lcd(40000,1)
		self.lcd.setModeAll(Lcd.NORMAL)
		self.lcd.setIntensityAll(5)
		self.lcd.setMaxDigits(0,3)
		self.lcd.setDecodeModeForDigits(0,[])
		self.lcd.setDigitValue(0,1,0)
		self.lcd.setDigitValue(0,0,0)
		self.lcd.setDigitValue(0,2,0)
		self.lcd.flush(0)
		self.Brightness = 15

	def activateLED(self, led):
		self.lcd.setDigitValue(0,0,0)
		self.lcd.setDigitValue(0,1,0)
		self.lcd.setDigitValue(0,2,0)
		self.lcd.setDigitValue(0,led[0],led[1])
		self.lcd.flush(0)

	def setBrightness(self, b):
		self.Brightness = b
		self.lcd.setIntensityAll(0,b)

