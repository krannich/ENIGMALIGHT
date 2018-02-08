import sys
import time 
import json
import math
import httplib
			
def popen():
	spidev = file('/usr/dk/aufruf.log', "wb")
	key = "144f42b9408f8fd112e2e757b11b4c17"
	ip = "192.168.1.99"
	url = '/api/' + key + '/lights/'
	lurl = url + '1/state'
	rurl = url + '2/state'

	while True:
		eingabe = sys.stdin.readline()

		if len(eingabe)>0:

			lr,lg,lb,rr,rg,rb,x = eingabe.split(' ')

			lr = float(lr)
			lg = float(lg)
			lb = float(lb)
			rr = float(rr)
			rg = float(rg)
			rb = float(rb)
			
			
			# Make red more vivid
			if lr > 0.04045:
				lr = float( math.pow((lr + 0.055) / (1.0 + 0.055), 2.4) )
			else:
				lr = float(lr / 12.92)

			if rr > 0.04045:
				rr = float( math.pow((rr + 0.055) / (1.0 + 0.055), 2.4))
			else:
				rr = float(rr / 12.92)


			# Make green more vivid
			if lg > 0.04045:
				lg = float( math.pow((lg + 0.055) / (1.0 + 0.055), 2.4) )
			else:
				lg = float(lr / 12.92)

			if rg > 0.04045:
				rg = float( math.pow((rg + 0.055) / (1.0 + 0.055), 2.4))
			else:
				rg = float(rg / 12.92)


			# Make blue more vivid
			if lb > 0.04045:
				lb = float( math.pow((lb + 0.055) / (1.0 + 0.055), 2.4) )
			else:
				lb = float(lb / 12.92)

			if rb > 0.04045:
				rb = float( math.pow((rb + 0.055) / (1.0 + 0.055), 2.4))
			else:
				rb = float(rb / 12.92)

			
			lxx = lr * 0.649926 + lg * 0.103455 + lb * 0.197109
			lyy = lr * 0.234327 + lg * 0.743075 + lb * 0.022598
			lzz = lr * 0.0000000 + lg * 0.053077 + lb * 1.035763
			lsum = lxx + lyy + lzz
			
			if lsum > 0:
				lx = lxx / lsum
				ly = lyy / lsum
			else:
				lx = 0
				ly = 0
			
			rxx = rr * 0.649926 + rg * 0.103455 + rb * 0.197109
			ryy = rr * 0.234327 + rg * 0.743075 + rb * 0.022598
			rzz = rr * 0.0000000 + rg * 0.053077 + rb * 1.035763
			rsum = rxx+ryy+rzz

			if rsum > 0:
				rx = rxx / rsum
				ry = ryy / rsum
			else:
				rx = 0
				ry = 0
			
			lparams = {'xy': [lx, ly], 'colormode': 'xy'}
			rparams = {'xy': [rx, ry], 'colormode': 'xy'}
			
			connection = httplib.HTTPConnection(ip, timeout=10)
			
			connection.request('PUT', lurl, json.dumps(lparams))
			response = connection.getresponse()
			
			connection.request('PUT', rurl, json.dumps(rparams))
			response = connection.getresponse()

			#data = response.read()

			connection.close()

   			#spidev.write("RGB left: " + str(lr*255) + ":" + str(lg*255) + ":" + str(lb*255) + "\n") 
			#spidev.write("RGB right: " + str(rr*255) + ":" + str(rg*255) + ":" + str(rb*255) + "\n") 
			
			#spidev.write("XY left: " + str(lx) + ":" + str(ly) + "\n")
			#spidev.write("XY right: " + str(rx) + ":" + str(ry) + "\n")

			#spidev.write("put: " + str(json.dumps(lparams)) + "\n")
			#spidev.write("data: " + str(data) + "\n")

			#spidev.write("-----------" + "\n")
			#spidev.flush()
	
		else:
			break
			
import time
time.sleep(7)
popen()