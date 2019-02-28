from panel.beacon import XPlaneBeaconListener
from panel.ecam import Ecam
import time

print ("Starting ECAM panel")
ecam = Ecam()

def xplaneDetectChange(stat, host):
	print ("Callback function ! Stat is %s", stat)
	if stat == XPlaneBeaconListener.LISTENING:
		(hostname, hostport) = host
		print ("x-plane host found : %s", hostname)
		ecam.startReceiver(hostname, hostport)
	else:
		print ("x-plane signal lost")
		ecam.stopReceiver()

print ("Starting beacon finder")
beacon = XPlaneBeaconListener()
beacon.registerChangeEvent(xplaneDetectChange)
beacon.start()

cont = True

while cont:
	try:
		cont = True
		time.sleep(1)
		ecam.test()
	except KeyboardInterrupt:
		print ("quitting...")
		cont = False

ecam.stop()
beacon.stop()
print ("Thread terminated !")
