#!/usr/bin/python
import socket
import sys
import time
import select
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
if len(sys.argv) != 4:
    print "Usage 1: milight-home.py <command> <device: 00-07-08> <zone: 01-04 or 00>"
    print "Usage 2: milight-home.py \"<full-command-9-bytes>\" <zone: 01-04 or 00>"
    print "Example usage 1: milight-home.py ON 07 00"
    print "Example usage 1: milight-home.py OFF 00 00"
    print "Example usage 2: milight-home.py CMD \"31 00 00 08 04 02 00 00 00\" 04"
    raise SystemExit(1)

# Some configuration settings
# NOTE: you should not touch them, except the UDP_TIMES_TO_SEND_COMMAND:
# increase this if you would encounter any issues
UDP_PORT = 5987 # UDP port on which we will communicate with the iBox
UDP_PORT_RECEIVE = 55054 # UDP port on which we will listen for responses
UDP_TIMES_TO_SEND_COMMAND = 5 # Number of times you want to send the UDP commands to the iBox
LOGFILE = "/home/pi/domoticz/scripts/milight-home.log" # Filename where some debug messages are written to

def log(message):
    debug_message = "[DEBUG - " + time.ctime() + "] " + message
    print debug_message
    logfile = open(LOGFILE, "a+")
    logfile.write(debug_message + "\n")
    logfile.close()

# The messages, V6 style
# See http://www.limitlessled.com/dev/ as reference and for examples

def get_command(usercommand, device, zone):
    """Returns the right iBox command, based on a argument which is passed in to the script"""
    command_dictionary = {
        "ON"            : "31 00 00 XX 03 01 00 00 00 YY 00",
        "OFF"           : "31 00 00 XX 03 02 00 00 00 YY 00",
        "BRIGHT0"       : "31 00 00 XX 02 00 00 00 00 YY 00",
        "BRIGHT25"      : "31 00 00 XX 02 19 00 00 00 YY 00",
        "BRIGHT50"      : "31 00 00 XX 02 32 00 00 00 YY 00",
        "BRIGHT75"      : "31 00 00 XX 02 4b 00 00 00 YY 00",
        "BRIGHT100"     : "31 00 00 XX 02 64 00 00 00 YY 00",
        "DISCO1"        : "31 00 00 XX 04 01 00 00 00 YY 00",
        "DISCO2"        : "31 00 00 XX 04 02 00 00 00 YY 00",
        "DISCO3"        : "31 00 00 XX 04 03 00 00 00 YY 00",
        "DISCO4"        : "31 00 00 XX 04 04 00 00 00 YY 00",
        "DISCO5"        : "31 00 00 XX 04 05 00 00 00 YY 00",
        "DISCO6"        : "31 00 00 XX 04 06 00 00 00 YY 00",
        "DISCO7"        : "31 00 00 XX 04 07 00 00 00 YY 00",
        "DISCO8"        : "31 00 00 XX 04 08 00 00 00 YY 00",
        "DISCO9"        : "31 00 00 XX 04 09 00 00 00 YY 00",
        "DISCOFASTER"   : "31 00 00 XX 03 02 00 00 00 YY 00",
        "DISCOSLOWER"   : "31 00 00 XX 03 01 00 00 00 YY 00",
        "WHITE"         : "31 00 00 XX 05 64 00 00 00 YY 00",
        "RED"           : "31 00 00 XX 01 00 00 00 00 YY 00",
        "GREEN"         : "31 00 00 XX 01 00 00 00 54 YY 00",
        "BLUE"          : "31 00 00 XX 01 00 00 00 BA YY 00",
        "AQUA"          : "31 00 00 XX 01 00 00 00 85 YY 00",   
        "YELLOW"        : "31 00 00 XX 01 00 00 00 3B YY 00",
    }
    command = command_dictionary.get(usercommand).replace("XX", device)
    command = command.replace("YY", zone)
    # Exception for the ON/OFF switch (= device type dependent...)
    if usercommand == "ON": 
        if device == "00":
            command = command[:15] + "03" + command[17:]
        elif device == "08":
            command = command[:12] + "04" + command[14:]
    elif usercommand == "OFF":
        if device == "00":
            command = command[:15] + "04" + command[17:]
        elif device == "08":
            command = command[:12] + "04" + command[14:]
    elif usercommand.startswith("BRIGHT"):
        if device == "08":
            command = command[:12] + "03" + command[14:]
    checksum = ('%x' % sum(int(x, 16) for x in command.split())).upper()
    return command + " " + checksum

# Completing the command when the user passed in a full 9 byte command
def get_command_from_user(full_command, zone):
    command = full_command + " " + zone
    checksum = ('%x' % sum(int(x, 16) for x in command.split())).upper()
    return command + " " + "00" + " " + checksum

def get_message(ibox_id1, ibox_id2, usercommand):
    """Builds a message."""
    return "80 00 00 00 11" + " " + ibox_id1 + " " + ibox_id2 + " " + "00 00 00" + " " + usercommand

# Below message is the first in a row, used to get the iBox identifiers
MESSAGE = "20 00 00 00 16 02 62 3A D5 ED A3 01 AE 08 2D 46 61 41 A7 F6 DC AF D3 E6 00 00 1E"

# Let's start :)
log("executing MiLight script... got the following arguments passed in: " + ' - '.join(sys.argv[1:]))

# STEP 1: send a UDP message to the iBox requesting the ibox identifiers and listen for a response
log("starting... sending message " + MESSAGE)
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCK.setblocking(0)
SOCK.bind(('', UDP_PORT_RECEIVE))
SOCK.sendto(bytearray.fromhex(MESSAGE), (UDP_IP, UDP_PORT))

READY = select.select([SOCK], [], [], 5) # We wait 5 seconds for an answer of the iBox
if READY[0]:
    DATA, ADDR = SOCK.recvfrom(1024)

    # STEP 2: get the ibox identifiers from the response
    RESPONSE = str(DATA.encode('hex'))
    IBOX_ID1 = RESPONSE[38:40]
    IBOX_ID2 = RESPONSE[40:42]
    log("received message: " + DATA.encode('hex'))
    log("received message: found iBoxID1 " + IBOX_ID1 + " and iBoxID2 " + IBOX_ID2)

    # STEP 3: get the actual message that should be sent
    if sys.argv[1] == "CMD":
        MESSAGE_COMMAND = get_message(IBOX_ID1, IBOX_ID2, get_command_from_user(sys.argv[2], sys.argv[3].zfill(2)))
    else:    
        MESSAGE_COMMAND = get_message(IBOX_ID1, IBOX_ID2, get_command(sys.argv[1], sys.argv[2].zfill(2), sys.argv[3].zfill(2)))
    log("sending the following message: " + MESSAGE_COMMAND)
    for x in range(0, UDP_TIMES_TO_SEND_COMMAND):
        log("sending attempt #" + str(x))
        SOCK.sendto(bytearray.fromhex(MESSAGE_COMMAND), (UDP_IP, UDP_PORT))
        log("sending attempt #" + str(x) + ": sent!")
    SOCK.close()

    log("messages are sent!")

raise SystemExit(0)
