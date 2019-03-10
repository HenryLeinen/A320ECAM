import RPi.GPIO as GPIO
import spidev


class Adc:

	def __init__(self, max_speed_hz):
		self.spi = spidev.SpiDev()
		self.spi.open(0,1)
		self.spi.max_speed_hz	= 40000 #max_speed_hz
		self.spi.lsbfirst = False
		self.spi.mode 		= 0b01
		self.spi.bits_per_word	= 8
		self.spi.cshigh		= False
		# Initialize the channel select pin
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(1, GPIO.OUT)
		GPIO.output(1, GPIO.LOW)

	def readInput(self, channel):
		if channel == 1:
			GPIO.output(1, GPIO.LOW)
		else:
			GPIO.output(1, GPIO.HIGH)
		sample = self.spi.readbytes(2)
		#print ("Sample read from channel %d: %s", channel, "{0:b}".format((sample[0]+sample[1]<<8)>>7))


