from panel.config import config
from panel.adc import Adc
from panel.ledstrip import LedStrip
from panel.keymatrix import Keyboard
from panel.led import Leds
from panel.xplane import xplane

class Ecam:
	# These are the different modes that the ECAM panel can maintain

	FIRST_CYCLE_MODE= 0
	MODE_ENG 	= 0
	MODE_APU 	= 6
	MODE_BLEED 	= 1
	MODE_COND	= 7
	MODE_PRESS	= 2
	MODE_DOOR	= 8
	MODE_ELEC	= 3
	MODE_WHEEL	= 9
	MODE_HYD	= 4
	MODE_FCTL	= 10
	MODE_FUEL	= 5
	LAST_CYCLE_MODE = 10
	MODE_STATUS	= 20

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

	def __init__(self, dbg=0):
		self.active = True
		self.dbg = dbg
		self.leds = Leds(3, 6)
		self.leds.setBrightness(5)
		self.adc = Adc(100000)
		self.adc.readInput(1)
		# Initialize the backlighting LED Strip
		self.ledstrip = LedStrip()
		# Initialize the Keyboard
		self.keys = Keyboard([2,3,4],[17,27,22,23,24,25])
		self.keys.registerCallbacks(self.onKeyPressed, 0)
		self.keys.start()
		# Initialize the ECAM modes
		self.mode = Ecam.MODE_STATUS
		self.mode_last = Ecam.MODE_ENG
		# Initialize the ECAM Clear and TO Config button states
		self.clr_on = False
		self.to_conf = False
		# Initialize the config file parser
		self.cfg = config()
		# load the configuration file
		self.cfg.load('config/xplane.cfg')
		#  Initialize the xplane receiver module
		self.xplane = xplane(self.cfg, dbg)	
		self.xplane.start()
		# Setup the callbacks for incoming mode changes
		self.xplane.setCallback("clr", self.cbkValueChanged)
		self.xplane.setCallback("mode", self.cbkValueChanged)
		self.xplane.setCallback("toconf", self.cbkValueChanged)
		self.modes = {
			"eng": Ecam.MODE_ENG,
			"apu": Ecam.MODE_APU,
			"bleed": Ecam.MODE_BLEED,
			"cond": Ecam.MODE_COND,
			"press": Ecam.MODE_PRESS,
			"door": Ecam.MODE_DOOR,
			"elec": Ecam.MODE_ELEC,
			"wheel": Ecam.MODE_WHEEL,
			"hyd": Ecam.MODE_HYD,
			"fctl": Ecam.MODE_FCTL,
			"fuel": Ecam.MODE_FUEL,
			"sts": Ecam.MODE_STATUS,
		}
		self.rev_modes = {
			Ecam.MODE_ENG: "eng",
			Ecam.MODE_APU: "apu",
			Ecam.MODE_BLEED: "bleed",
			Ecam.MODE_COND: "cond",
			Ecam.MODE_PRESS: "press",
			Ecam.MODE_DOOR: "door",
			Ecam.MODE_ELEC: "elec",
			Ecam.MODE_WHEEL: "wheel",
			Ecam.MODE_HYD: "hyd",
			Ecam.MODE_FCTL: "fctl",
			Ecam.MODE_FUEL: "fuel",
			Ecam.MODE_STATUS: "sts",
		}

	def cbkValueChanged(self, idx, newval):
		print ("***** CALLBACK on index " + str(idx) + " with value " + str(newval))
		if idx == "clr":
			self.clr_on = newval
		elif idx == "mode":
			self.mode = self.modes[newval]
		elif idx == "toconf":
			self.to_conf = newval
		self.updateStatus()

	def onKeyPressed(self, key):
		if key == Keyboard.BTN_ENG:
			print ("BTN_ENG pressed")
			self.mode = Ecam.MODE_ENG
			self.xplane.setValue("mode", "eng")
		elif key == Keyboard.BTN_APU:
			print ("BTN_API pressed")
			self.mode = Ecam.MODE_APU
			self.xplane.setValue("mode", "apu")
		elif key == Keyboard.BTN_BLEED:
			print ("BTN_BLEED pressed")
			self.mode = Ecam.MODE_BLEED
			self.xplane.setValue("mode", "bleed")
		elif key == Keyboard.BTN_COND:
			print ("BTN_COND pressed")
			self.mode = Ecam.MODE_COND
			self.xplane.setValue("mode", "cond")
		elif key == Keyboard.BTN_PRESS:
			print ("BTN_PRESS pressed")
			self.mode = Ecam.MODE_PRESS
			self.xplane.setValue("mode", "press")
		elif key == Keyboard.BTN_DOOR:
			print ("BTN_DOOR pressed")
			self.mode = Ecam.MODE_DOOR
			self.xplane.setValue("mode", "door")
		elif key == Keyboard.BTN_ELEC:
			print ("BTN_ELEC pressed")
			self.mode = Ecam.MODE_ELEC
			self.xplane.setValue("mode", "elec")
		elif key == Keyboard.BTN_WHEEL:
			print ("BTN_WHEEL pressed")
			self.mode = Ecam.MODE_WHEEL
			self.xplane.setValue("mode", "wheel")
		elif key == Keyboard.BTN_HYD:
			print ("BTN_HYD pressed")
			self.mode = Ecam.MODE_HYD
			self.xplane.setValue("mode", "hyd")
		elif key == Keyboard.BTN_FCTL:
			print ("BTN_FCTL pressed")
			self.mode = Ecam.MODE_FCTL
			self.xplane.setValue("mode", "fctl")
		elif key == Keyboard.BTN_FUEL:
			print ("BTN_FUEL pressed")
			self.mode = Ecam.MODE_FUEL
			self.xplane.setValue("mode", "fuel")
		elif key == Keyboard.BTN_STS:
			print ("BTN_STATUS pressed")
			# store the last valid mode, only if it was not status
			# this is for the use case, that the user presses the ALL button
			# in which the panel will cycle through all modes (except STATUS)
			# so we need to remember which was the last valid mode before pressing
			# STATUS
			if self.mode != Ecam.MODE_STATUS:
				self.mode_last = self.mode
			self.mode = Ecam.MODE_STATUS
			self.xplane.setValue("mode", "sts")
			self.clr_on = False
		elif key == Keyboard.BTN_CLR:
			print ("BTN_CLR left was pressed")
			if self.clr_on == True:
				self.clr_on = False
			else:
				self.clr_on = True
			self.xplane.setValue("clr", self.clr_on)
		elif key == Keyboard.BTN_CLR2:
			print ("BTN_CLR right was pressed")
			if self.clr_on == True:
				self.clr_on = False
			else:
				self.clr_on = True
			self.xplane.setValue("clr", self.clr_on)
		elif key == Keyboard.BTN_ALL:
			print ("BTN_ALL was pressed")
			if self.mode != Ecam.MODE_STATUS:
				self.mode = self.mode + 1
			else:
				self.mode = self.mode_last + 1
			if self.mode > Ecam.LAST_CYCLE_MODE:
				self.mode = Ecam.FIRST_CYCLE_MODE
			self.xplane.setValue("mode", self.rev_modes[self.mode])
		elif key == Keyboard.BTN_TO_CONFIG:
			print ("BTN_TO_CONFIG was pressed")
			if self.to_conf == True:
				self.to_conf = False
			else:
				self.to_conf = True
			self.xplane.setValue("toconf", self.to_conf)
		self.updateStatus()

	def updateStatus(self):
		actvLeds = []
		if self.clr_on == True:
			actvLeds.append(Ecam.LED_CLR_L)
			actvLeds.append(Ecam.LED_CLR_R)
		if self.to_conf == True:
			actvLeds.append(Ecam.LED_TOCONF)
		if self.mode == Ecam.MODE_ENG:
			print ("Mode MODE_ENG activated")
			actvLeds.append(Ecam.LED_ENG)
		elif self.mode == Ecam.MODE_APU:
			print ("Mode MODE_APU activated")
			actvLeds.append(Ecam.LED_APU)
		elif self.mode == Ecam.MODE_BLEED:
			print ("Mode MODE_BLEED activated")
			actvLeds.append(Ecam.LED_BLEED)
		elif self.mode == Ecam.MODE_COND:
			print ("Mode MODE_CON activated")
			actvLeds.append(Ecam.LED_COND)
		elif self.mode == Ecam.MODE_PRESS:
			print ("Mode MODE_PRESS activated")
			actvLeds.append(Ecam.LED_PRESS)
		elif self.mode == Ecam.MODE_DOOR:
			print ("Mode MODE_DOOR activated")
			actvLeds.append(Ecam.LED_DOOR)
		elif self.mode == Ecam.MODE_ELEC:
			print ("Mode MODE_ELEC activated")
			actvLeds.append(Ecam.LED_ELEC)
		elif self.mode == Ecam.MODE_WHEEL:
			print ("Mode MODE_WHEEL activated")
			actvLeds.append(Ecam.LED_WHEEL)
		elif self.mode == Ecam.MODE_HYD:
			print ("Mode MODE_HYD acticated")
			actvLeds.append(Ecam.LED_HYD)
		elif self.mode == Ecam.MODE_FCTL:
			print ("Mode MODE_FCTL activated")
			actvLeds.append(Ecam.LED_FCTL)
		elif self.mode == Ecam.MODE_FUEL:
			print ("Mode MODE_FUEL activated")
			actvLeds.append(Ecam.LED_FUEL)
		elif self.mode == Ecam.MODE_STATUS:
			print ("Mode MODE_STATUS activated")
			actvLeds.append(Ecam.LED_STS)
		self.leds.activateLEDs(actvLeds)

	def stop(self):
		self.keys.stop()
		self.xplane.stop()
		print ("...ECAM terminated...")

	def test(self):
		pass
		self.adc.readInput(1)
		self.adc.readInput(2)
