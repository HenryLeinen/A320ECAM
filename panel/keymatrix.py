import RPi.GPIO as GPIO
import time
import threading


class Keyboard(threading.Thread):
	# mapping info
	BTN_ENG 	= 0x04
	BTN_APU 	= 0x14
	BTN_CLR 	= 0x24

	BTN_EMER_CANC 	= 0x05
	BTN_BLEED 	= 0x15
	BTN_COND	= 0x25

	BTN_PRESS 	= 0x03
	BTN_DOOR	= 0x13
	BTN_STS		= 0x23

	BTN_ELEC	= 0x02
	BTN_WHEEL	= 0x12
	BTN_RCL		= 0x22

	BTN_TO_CONFIG	= 0x01
	BTN_HYD 	= 0x11
	BTN_FCTL 	= 0x21

	BTN_FUEL	= 0x00
	BTN_ALL		= 0x10
	BTN_CLR2	= 0x20

	def __init__(self, cols, rows):
		threading.Thread.__init__(self)
		self.keys = [[0 for y in range(len(rows))] for x in range(len(cols))]
		# initialize the GPIO
		GPIO.setmode(GPIO.BCM)
		for c in cols:
			GPIO.setup(c, GPIO.OUT)
			GPIO.output(c, GPIO.HIGH)

		for r in rows:
			GPIO.setup(r, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		self.cols = cols
		self.rows = rows
		self.col = len(cols)-1
		self.maxcol = self.col+1

		self.active = True
		self.callbackPressed = 0
		self.callbackReleased = 0
		self.ack = False

	def registerCallbacks(self, cbkPressed, cbkReleased):
		self.callbackPressed = cbkPressed
		self.callbackReleased = cbkReleased

	def updateStatus(self, col, rows):
		# walk through the rows read data
		for idx, r in enumerate(rows):
			# check if the respective value has changed since last time
			if self.keys[col][idx] != r:
				# value was changed since last time, so store it for the next iteration
				self.keys[col][idx] = r
				kk = (col << 4) + idx
				if r == GPIO.LOW:
					if self.callbackPressed != 0:
						self.callbackPressed(kk)
#					print ("Key %02x was pressed" % kk)
				else:
					if self.callbackReleased != 0:
						self.callbackReleased(kk)
#					print ("Key %02x was released" % kk)



	def run(self):
		while self.active == True:
			# deactivate prev column
			GPIO.output(self.cols[self.col], GPIO.HIGH)
			# increment pointer to next column
			self.col = self.col + 1
			if self.col > self.maxcol-1:
				self.col = 0
			# Activate next column
			GPIO.output(self.cols[self.col], GPIO.LOW)
			# wait shortly
			time.sleep(0.040)
			# read status of rows into array rr
			rr = []
			for r in self.rows:
				rr.append( GPIO.input(r) )

			# use the read array and sort out, which keys are pressed and which one is released
			self.updateStatus(self.col, rr)
		self.ack = True

	def stop(self):
		print ("*** Keyboard terminating")
		self.active = False
		while self.ack == False:
			time.sleep(0.04)
		GPIO.cleanup()



