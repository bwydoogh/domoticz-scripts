# Domoticz scripts 
## Milight Python script (API V6 - setup: Milight iBox + RGBW bulbs)
This Python script is able to communicate with a iBox (**API version v6**; see http://www.limitlessled.com/dev/). **The script can turn on or off all lights (all zones), including the iBox, as well as changing the brightness and activating the DISCO mode.** This script works perfect in combination with a **virtual switch** (ON/OFF) in Domoticz.


Steps to follow:

1. Put the script in your Domoticz scripts folder
2. Change the IP address of the iBox controller in the script: variable **UDP_IP**
3. Add a virtual/dummy switch in Domoticz (see https://www.domoticz.com/wiki/Wemo#Creating_Dummy_Switches)
4. The ON action of the dummy switch could be set to: `script:///<script location>/milight-home.sh ON`
This action will turn on the lights of the bulbs **and** the iBox. If you only want to have the bulbs on, execute the script as follows (_put a device identifier (00 (=iBox), 07 (= RGBWW) or 08 (=RGBW)) as last argument_): `script:///<script location>/milight-home.sh ON 07` or `script:///<script location>/milight-home.sh ON 08`
5. The OFF action of the dummy switch could be set to: `script:///<script location>/milight-home.sh OFF`
    
The script can also be executed in standalone mode of course: 

    $ python milight-home.py ON <device> (<device> = 00, 07 or 08)
    $ python milight-home.py OFF <device> (<device> = 00, 07 or 08)
    $ python milight-home.py DISCO1 <device>
    $ python milight-home.py <command> <device> (see below for the list of valid <command>)

Complete list of arguments (besides ON and OFF):

    ON/OFF/DISCO[1-9]/DISCOFASTER/DISCOSLOWER/WHITE/BRIGHT[0-25-50-75-100]
