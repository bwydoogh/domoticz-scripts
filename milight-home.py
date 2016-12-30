#!/usr/bin/python
import socket,sys;

# Let's check if an argument ON or OFF is passed in to the script; if not we stop...
if len(sys.argv) == 1:
    print "Usage: ON or OFF? Please specify as argument"
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
else:
    MESSAGE_COMMAND = MESSAGE_LIGHTS_OFF.replace("I1", iboxId1)
    MESSAGE_COMMAND = MESSAGE_COMMAND.replace("I2", iboxId2)
    MESSAGE_COMMAND_IBOX = MESSAGE_IBOXLT_OFF.replace("I1", iboxId1)
    MESSAGE_COMMAND_IBOX = MESSAGE_COMMAND_IBOX.replace("I2", iboxId2)

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
