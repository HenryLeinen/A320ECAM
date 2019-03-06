from configparser import ConfigParser
from panel.beacon import XPlaneBeaconListener
import socket
import struct
import sys
import threading

class xplane(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.active = True
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
		self.cfg["Requests"] = {
			b"sim/custom/xap/ewd_clr\x00": 1
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
		# start listening for the X-Plane beacon, which tells us where x-plane is currently running
		self.beacon = XPlaneBeaconListener()
		self.beacon.registerChangeEvent(self.xPlaneHostChange)
		self.beacon.start()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.sock.settimeout(3.0)
		self.UDP_XPL = ("localhost", 49009)
		self.UDP_LCL = ("", 49009)
		self.sock.bind(self.UDP_LCL)
		# prepare all internal lookup tables for datarefs and callbacks
		self.datarefs = {}
		self.datarefidx = 0
		self.xplaneValues = {}
		self.callbacks = {}

	def setCallback(self, var, cbk):
		self.callbacks[var] = cbk

	def xPlaneHostChange(self, stat, host):
		if stat == XPlaneBeaconListener.LISTENING:
			(hostname,hostport) = host
			print ("X-Plane instance found on %s:%d", hostname, hostport)
			# start the receiver
			self.UDP_XPL = (socket.gethostbyname(hostname),hostport)
			self.UDP_LCL = ("localhost",49009)
			self.startReceiver()
		else:
			# stop the receiver
			print ("X-Plane signal lost !")
			self.UDP_XPL = ("localhost", 49009)
			self.stopReceiver()

	def stop(self):
		self.active = False
		# stop the beacon
		self.beacon.stop()
		# shutdown the socket
		self.sock.close()
		# stop the receiver
		self.stopReceiver()

	def sendValue(self, dataref, value):
		cmd = b"DREF\x00"
		string = dataref.encode()
		message = struct.pack("<5sf500s", cmd, value, string)
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

	def request(self, dataref, freq=None):
		if freq == None:
			freq = 1
		# check whether or not this has already been requested
		if dataref in self.datarefs.values():
			# yes, it's there so get the index
			idx = list(self.datarefs.keys()) [list(self.datarefs.values()).index(dataref)]
			# check if dataref also exists in the xplaneValues
			if dataref in self.xplaneValues.keys():
				del self.xplaneValues[dataref]
			del self.datarefs[idx]
		else:
			idx = self.datarefidx
			self.datarefs[self.datarefidx] = dataref
			self.datarefidx += 1
			self.xplaneValues[dataref] = 0
		cmd = b"RREF\x00"
		string = dataref.encode()
		print ("Requesting dataref %s using index %d", dataref, idx)
		message = struct.pack("<5sii400s", cmd, freq, idx, string)
		self.sock.sendto(message, self.UDP_XPL)

	def subscribe(self):
		self.request(b"sim/custom/xap/ewd_clr\x00")

	def startReceiver(self):
		# Subscribe to the datarefs
		self.subscribe()

	def stopReceiver(self):
		pass


	def parse(self, retvalues):
		print ("Parsing ", retvalues)
		for idx in retvalues:
			if idx in self.xplaneValues.keys():
				orgval = self.xplaneValues[idx]
				newval = retvalues[idx]
				if orgval != newval:
					print ("Value " + idx + " has changed from " + str(orgval) + " to " + str(newval))
					# trigger change notification
					self.xplaneValues[idx] = newval
					# call callback function if existing
					if idx in self.callbacks.keys():
						print ("Calling callback for %s" % idx)
						self.callbacks[idx](idx, newval)
					else:
						print ("No callback for %s" % idx)
				else:
					print ("Value did not change")
			else:
				self.xplaneValues[idx] = newval
				print ("################ Unknown dataref received %s" % idx)


	def run(self):
		print ("Starting receiver loop")
		while self.active == True:
			try:
				# receive a packet
				data = self.sock.recv(1024)
				# temporary collection of values
				retvalues = {}
				# read the header of the message
				header = data[0:4]
				if header == b"RREF":
					# we get 8 bytes for each dataref
					# an integer for the idx and the float value
					values = data[5:]
					num_values = int(len(values)/8)

					# extract all received values
					for i in range(0, num_values):
						# extract each individual value from the stream
						singledata = values[i*8:(i+1)*8]
						(idx, fval) = struct.unpack("<if", singledata)
						print ("Item with index %d found" %idx)
						if idx in self.datarefs.keys():
							retvalues[self.datarefs[idx]] = fval
					# parse the values to find out what changes we received
					self.parse(retvalues)
				elif header == b"RPOS":
					print ("Position information rececived !")
				elif header == b"DATA":
					print ("DATA block received !")
				else:
					print ("Unknown packet received !", data[0:4])
			except socket.timeout:
				print ("*********PING********")
				pass
			except socket.error:
				print ("Socket error !")
				pass
			except :
				print ("Bullshit exception")
				raise
		print ("Terminating receiver loop")
		self.sock.close()

