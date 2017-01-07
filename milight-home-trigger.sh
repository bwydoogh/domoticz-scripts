#!/bin/bash
if [[ "$1" == "ON" ]] || [[ "$1" == "OFF" ]]
then
    /home/pi/domoticz/scripts/milight-home.py "$1" 00 && sleep .5 && /home/pi/domoticz/scripts/milight-home.py "$1" 07
else
    /home/pi/domoticz/scripts/milight-home.py "$1" "$2"
fi
