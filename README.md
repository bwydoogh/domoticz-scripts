# Domoticz scripts 
## Milight Python script (API V6 - setup: Milight iBox + RGBW bulbs)
This Python script is able to communicate with a iBox (**API version v6**; see http://www.limitlessled.com/dev/). The script can turn on or off all lights (all zones), including the iBox. This script works perfect in combination with a **virtual switch** (ON/OFF) in Domoticz.

Steps to follow:

1. Put the script in your Domoticz scripts folder
2. Change the IP address of the iBox controller in the script: variable **UDP_IP**
3. Add a virtual/dummy switch in Domoticz (see https://www.domoticz.com/wiki/Wemo#Creating_Dummy_Switches)
4. The ON action of the dummy switch should be set to: `script:///<script location>/milight-home ON`
5. The OFF action of the dummy switc should be set to: `script:///<script location>/milight-home OFF`
    
The script can also be executed in standalone mode of course: 

    $ python milight-home.py ON
    $ python milight-home.py OFF

⚠ This is _work in progress_: zone control, dimming, color setting... are not implemented yet.
