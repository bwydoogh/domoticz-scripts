#!/usr/bin/python
import socket,sys;

# FOR BETTER COMPATIBILITY FOR COLOR INTRODUCTION FROM COLOR PICKER WE NEED TO ADD A CHECKSUM CALCULATOR : CS
#MESSAGE_LIGHTS_ON  = "80 00 00 00 11 I1 I2 00 00 00 31 00 00 07 03 01 00 00 00 00 00 CS"
#CS CALCULATION IS : 31+00+00+07+03+01+00+00+00+00+00=3C

# Let's check if an argument ON or OFF is passed in to the script; if not we stop...
if len(sys.argv) == 1:
    print "Usage: please specify a valid argument (ON/OFF/DISCO[1-9]/DISCOFASTER/DISCOSLOWER/WHITE/BRIGHT[0-25-50-75-100]."
    raise SystemExit(1)

# Some configuration settings
# iBox IP (and UDP port 5987)
UDP_IP = "192.168.2.170"
UDP_PORT = 5987
# UDP port on which we will listen for responses
UDP_PORT_RECEIVE = 55054
# Number of times you want to send the UDP commands to the iBox
# NOTE: only use this when you don't always have a result; not sure what exactly causes this issue
UDP_TIMES_TO_SEND_COMMAND = 5

# The messages, V6 style
# See http://www.limitlessled.com/dev/ as reference and for examples
MESSAGE = "20 00 00 00 16 02 62 3A D5 ED A3 01 AE 08 2D 46 61 41 A7 F6 DC AF D3 E6 00 00 1E"
MESSAGE_LIGHTS_ON  = "80 00 00 00 11 I1 I2 00 00 00 31 00 00 07 03 01 00 00 00 00 00 3C"
MESSAGE_IBOXLT_ON  = "80 00 00 00 11 I1 I2 00 00 00 31 00 00 00 03 03 00 00 00 00 00 37"
MESSAGE_LIGHTS_OFF = "80 00 00 00 11 I1 I2 00 00 00 31 00 00 07 03 02 00 00 00 00 00 3D"
MESSAGE_IBOXLT_OFF = "80 00 00 00 11 I1 I2 00 00 00 31 00 00 00 03 04 00 00 00 00 00 38"

# DISCO CONTROL FOR IBOX
MESSAGE_IBOXLT_DISCOFASTER = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 03 02 00 00 00 01 00 37"
MESSAGE_IBOXLT_DISCOSLOWER = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 03 01 00 00 00 01 00 36"
MESSAGE_IBOXLT_DISCO1 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 04 01 00 00 00 01 00 37"
MESSAGE_IBOXLT_DISCO2 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 04 02 00 00 00 01 00 38"
MESSAGE_IBOXLT_DISCO3 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 04 03 00 00 00 01 00 39"
MESSAGE_IBOXLT_DISCO4 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 04 04 00 00 00 01 00 3A" 
MESSAGE_IBOXLT_DISCO5 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 04 05 00 00 00 01 00 3B" 
MESSAGE_IBOXLT_DISCO6 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 04 06 00 00 00 01 00 3C" #RED ALERT
MESSAGE_IBOXLT_DISCO7 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 04 07 00 00 00 01 00 3D" #GREEN ALERT
MESSAGE_IBOXLT_DISCO8 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 04 08 00 00 00 01 00 3E" #BLUE ALERT
MESSAGE_IBOXLT_DISCO9 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 04 09 00 00 00 01 00 3F" #WHITE ALERTE

#SET TO COLOR
MESSAGE_IBOXLT_WHITE =  	"80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 03 05 00 00 00 01 00 3A" #WHITE
MESSAGE_IBOXLT_RED =    	"80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 01 00 00 00 00 01 00 33" #RED
MESSAGE_IBOXLT_GREEN =  	"80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 01 00 00 00 54 01 00 87" #GREEN
MESSAGE_IBOXLT_BLUE =   	"80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 01 00 00 00 BA 01 00 ED" #BLUE
MESSAGE_IBOXLT_AQUA =       "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 01 00 00 00 85 01 00 B8" #AQUA


#BRIGHTNESS
MESSAGE_IBOXLT_BRIGHT0 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 02 00 00 00 00 01 00 34" #0%
MESSAGE_IBOXLT_BRIGHT25 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 02 19 00 00 00 01 00 4d" #25%
MESSAGE_IBOXLT_BRIGHT50 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 02 32 00 00 00 01 00 66" #50%
MESSAGE_IBOXLT_BRIGHT75 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 02 4b 00 00 00 01 00 7f" #75%
MESSAGE_IBOXLT_BRIGHT100 = "80 00 00 00 11 I1 I2 E6 80 00 31 00 00 00 02 64 00 00 00 01 00 98" #100%

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', UDP_PORT_RECEIVE))
sock.sendto(bytearray.fromhex(MESSAGE), (UDP_IP, UDP_PORT))
sock.close()

sockreceive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockreceive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockreceive.bind(('', UDP_PORT_RECEIVE))

data, addr = sockreceive.recvfrom(65536)
print "[DEBUG]received message:", data.encode('hex') 
sockreceive.close()
response = str(data.encode('hex'))
iboxId1 = response[38:40]
iboxId2 = response[40:42]
print "[DEBUG]requesting iBox to execute command", iboxId1
print "[DEBUG]requesting iBox to execute command", iboxId2

# Preparing the messages to sent
# NOTE: one message to the RGBWW bulbs (07 in the command) and one message to the iBox (00 instead of 07 in the command)
if sys.argv[1] == "ON":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)	

elif sys.argv[1] == "OFF":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_OFF.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_OFF.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "DISCO1":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCO1.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "DISCO2":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCO2.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "DISCO3":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCO3.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)

elif sys.argv[1] == "DISCO4":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCO4.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "DISCO5":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCO5.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)

elif sys.argv[1] == "DISCO6":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCO6.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)

elif sys.argv[1] == "DISCO7":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCO7.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "DISCO8":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCO8.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "DISCO9":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCO9.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "DISCOFASTER":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCOFASTER.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "DISCOSLOWER":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_DISCOSLOWER.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)

elif sys.argv[1] == "WHITE":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_WHITE.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "BRIGHT0":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_BRIGHT0.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "BRIGHT25":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_BRIGHT25.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "BRIGHT50":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_BRIGHT50.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "BRIGHT75":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_BRIGHT75.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "BRIGHT100":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_BRIGHT100.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "RED":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_RED.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "BLUE":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_BLUE.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "GREEN":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_GREEN.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)
	
elif sys.argv[1] == "AQUA":
    MESSAGE_COMMAND = MESSAGE_LIGHTS_ON.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_AQUA.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)


else:
    print "No valid argument passed in. See usage"
    raise SystemExit(1)


else:
    print "No valid argument passed in. See usage"
    raise SystemExit(1)


print "[DEBUG]sending message to the smart bulbs:", MESSAGE_COMMAND
print "[DEBUG]sending message to the iBox:", MESSAGE_COMMAND_IBOX

socksendto = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socksendto.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socksendto.bind(('', UDP_PORT_RECEIVE))
for x in range(0, UDP_TIMES_TO_SEND_COMMAND):
    socksendto.sendto(bytearray.fromhex(MESSAGE_COMMAND), (UDP_IP, UDP_PORT))
socksendto.close()

socksendtoibox = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socksendtoibox.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socksendtoibox.bind(('', UDP_PORT_RECEIVE))
for x in range(0, UDP_TIMES_TO_SEND_COMMAND):
    socksendtoibox.sendto(bytearray.fromhex(MESSAGE_COMMAND_IBOX), (UDP_IP, UDP_PORT))
socksendtoibox.close()

print "[DEBUG]message(s) sent!"

raise SystemExit(0)
