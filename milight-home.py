#!/usr/bin/python
import socket
import sys
"""
Small Python script allowing communication with an iBox controller.
Can be used as a virtual switch in Domoticz.
"""
__author__ = "Benny Wydooghe"
__email__ = "benny.wydooghe@gmail.com"

# iBOX IP address - CHANGE THIS TO THE IP-ADDRESS OF YOUR iBOX
UDP_IP = "192.168.2.170"

# Let's check if an argument ON or OFF is passed in to the script; if not we stop...
# Usage: milight-home.py <command> <device>
if len(sys.argv) != 3:
    print "Usage: milight-home.py <command> <device>"
    print "Examples: milight-home.py ON 07, milight-home.py OFF 00"
    raise SystemExit(1)

# Some configuration settings
# NOTE: you should not touch them, except the UDP_TIMES_TO_SEND_COMMAND:
# increase this if you would encounter any issues
UDP_PORT = 5987 # UDP port on which we will communicate with the iBox
UDP_PORT_RECEIVE = 55054 # UDP port on which we will listen for responses
UDP_TIMES_TO_SEND_COMMAND = 5 # Number of times you want to send the UDP commands to the iBox

# The messages, V6 style
# See http://www.limitlessled.com/dev/ as reference and for examples

def get_command(usercommand, device):
    """Returns the right iBox command, based on a argument which is passed in to the script"""
    command_dictionary = {
        "ON"            : "31 00 00 XX 03 01 00 00 00 00 00",
        "OFF"           : "31 00 00 XX 03 02 00 00 00 00 00",
        "BRIGHT0"       : "31 00 00 XX 02 00 00 00 00 01 00 34",
        "BRIGHT25"      : "31 00 00 XX 02 19 00 00 00 01 00 4D",
        "BRIGHT50"      : "31 00 00 XX 02 32 00 00 00 01 00 66",
        "BRIGHT75"      : "31 00 00 XX 02 4b 00 00 00 01 00 7F",
        "BRIGHT100"     : "31 00 00 XX 02 64 00 00 00 01 00 98",
        "DISCO1"        : "31 00 00 XX 04 01 00 00 00 01 00 37",
        "DISCO2"        : "31 00 00 XX 04 02 00 00 00 01 00 38",
        "DISCO3"        : "31 00 00 XX 04 03 00 00 00 01 00 39",
        "DISCO4"        : "31 00 00 XX 04 04 00 00 00 01 00 3A",
        "DISCO5"        : "31 00 00 XX 04 05 00 00 00 01 00 3B",
        "DISCO6"        : "31 00 00 XX 04 06 00 00 00 01 00 3C",
        "DISCO7"        : "31 00 00 XX 04 07 00 00 00 01 00 3D",
        "DISCO8"        : "31 00 00 XX 04 08 00 00 00 01 00 3E",
        "DISCO9"        : "31 00 00 XX 04 09 00 00 00 01 00 3F",
        "DISCOFASTER"   : "31 00 00 XX 03 02 00 00 00 01 00 37",
        "DISCOSLOWER"   : "31 00 00 XX 03 01 00 00 00 01 00 36",
        "WHITE"         : "31 00 00 XX 03 05 00 00 00 01 00 3A",
        "RED"           : "31 00 00 XX 01 00 00 00 00 01 00 33",
        "GREEN"         : "31 00 00 XX 01 00 00 00 54 01 00 87",
        "BLUE"          : "31 00 00 XX 01 00 00 00 BA 01 00 ED",
        "AQUA"          : "31 00 00 XX 01 00 00 00 85 01 00 B8",
    }
    command = command_dictionary.get(usercommand).replace("XX", device)
    # Exception for the ON/OFF switch of the iBox
    if usercommand == "ON" and device == "00":
        command = command[:15] + "03" + command[17:]
    elif usercommand == "OFF" and device == "00":
        command = command[:15] + "04" + command[17:]
    checksum = ('%x' % sum(int(x, 16) for x in command.split())).upper()
    return command + " " + checksum

def get_message(ibox_id1, ibox_id2, usercommand):
    """Builds a message."""
    return "80 00 00 00 11" + " " + ibox_id1 + " " + ibox_id2 + " " + "00 00 00" + " " + usercommand

# Below message is the first in a row, used to get the iBox identifiers
MESSAGE = "20 00 00 00 16 02 62 3A D5 ED A3 01 AE 08 2D 46 61 41 A7 F6 DC AF D3 E6 00 00 1E"

# Let's start :)
# STEP 1: send a UDP message to the iBox requesting the ibox identifiers and listen for a response
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCK.bind(('', UDP_PORT_RECEIVE))
SOCK.sendto(bytearray.fromhex(MESSAGE), (UDP_IP, UDP_PORT))
DATA, ADDR = SOCK.recvfrom(1024)

# STEP 2: get the ibox identifiers from the response
RESPONSE = str(DATA.encode('hex'))
IBOX_ID1 = RESPONSE[38:40]
IBOX_ID2 = RESPONSE[40:42]
print "[DEBUG] received message: ", DATA.encode('hex')
print "[DEBUG] received message - ibox identifier 1: ", IBOX_ID1
print "[DEBUG] received message - ibox identifier 2: ", IBOX_ID2

# STEP 3: get the actual message that should be sent
MESSAGE_COMMAND = get_message(IBOX_ID1, IBOX_ID2, get_command(sys.argv[1], sys.argv[2]))
print "[DEBUG] sending the following message: ", MESSAGE_COMMAND
for x in range(0, UDP_TIMES_TO_SEND_COMMAND):
    SOCK.sendto(bytearray.fromhex(MESSAGE_COMMAND), (UDP_IP, UDP_PORT))
SOCK.close()

print "[DEBUG] message(s) sent!"

raise SystemExit(0)
