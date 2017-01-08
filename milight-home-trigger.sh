#!/bin/bash
if [[ "$1" == "ON" ]] || [[ "$1" == "OFF" ]]
then
    # Special case: turn all (including the iBox) leds ON or OFF
    # What happens are 2 script calls, once for each device type (currently 00 and 07)
    /home/pi/domoticz/scripts/milight-home.py "$1" 00 && sleep .5 && /home/pi/domoticz/scripts/milight-home.py "$1" 07
else
    # Regular case: pass all arguments to the Python script
    /home/pi/domoticz/scripts/milight-home.py "$@"
fi
