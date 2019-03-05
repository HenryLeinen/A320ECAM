from configparser import ConfigParser
import socket
import struct
import sys

class xplane:

	def __init__(self):
		# Initialize the config file parser
		self.cfg = ConfigParser()

		# Setup the default structure of the mapping and the config file
		self.cfg["Variables"] = {
			"Mode":  b"sim/custom/xap/disp/sys/mode\x00",			# e.g. "sim/custom/xap/disp/sys/mode"
			"Clr":   b"sim/custom/xap/ewd_clr\x00",				# e.g. "sim/custom/xap/ewd_clr"
			"All":   b"sim/custom/xap/ewd_all\x00",				# e.g. "sim/custom/xap/ewd_all"
			"BrightnessUpperDisplay": b"sim/custom/xap/lght_upd\x00",		# e.g. "sim/custom/xap/lght_upd"
			"BrightnessLowerDisplay": b"sim/custom/xap/lght_dnd\x00"		# e.g. "sim/custom/xap/lght_dnd"
		}
		self.cfg["States"] = {
			"ENG":		11.0,
			"APU":		2.0,
			"BLEED":	7.0,
			"COND":		8.0,
			"PRESS":	3.0,
			"DOOR":		9.0,
			"WHEEL":	5.0,
			"ELEC":		6.0,
			"FCTL":		4.0,
			"HYD":		0.0,
			"FUEL":		1.0
		}

	def setConnectionDetails(self, xp_host='localhost', xp_port=49009, local_port=49009):
		# setup the socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.settimeout(3.0)
		self.UDP_XPL = (socket.gethostbyname(xp_host),xp_port)
		self.UDP_LCL = ("",local_port)

	def sendValue(self, dataref, value):
		cmd = b"DREF\x00"
		string = dataref.encode()
#		string = '{1}\x00{2}'.format(dataref, '{:x^500}'.format(' '))
		message = struct.pack("<5sf500s", cmd, value, string)
		print ("Sending " + dataref + " with value " + str(value))
		assert(len(message)==509)
		self.sock.sendto(message, self.UDP_XPL)

	def setMode(self, mode):
		val = self.cfg["States"][mode]
		self.sendValue(self.cfg["Variables"]["Mode"], float(val))

	def setBrightnessUpper(self, val):		# val ranges from 0 to 1
		val = 10.0 - val*10.0
		self.sendValue(self.cfg["Variables"]["BrightnessUpperDisplay"], float(val))

	def setBrightnessLower(self, val):		# val ranges from 0 to 1
		val = 10.0 - val*10.0
		self.sendValue(self.cfg["Variables"]["BrightnessLowerDisplay"], float(val))

	def setClear(self, val):
		self.sendValue(self.cfg["Variables"]["Clr"], float(val))
