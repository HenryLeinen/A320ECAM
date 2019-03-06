from panel.ecam import Ecam
import time

print ("Starting ECAM panel")
ecam = Ecam()

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
print ("Thread terminated !")
