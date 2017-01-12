# Domoticz scripts 
## Milight Python script (API V6 - setup: Milight iBox + RGBW bulbs)
This Python script is able to communicate with a iBox (**API version v6**; see http://www.limitlessled.com/dev/). **The script can turn on or off all lights (all zones), including the iBox, as well as changing the brightness and activating the DISCO mode.** This script works perfect in combination with a **virtual switch** (ON/OFF) in Domoticz.


### Domoticz integration ###

1. Put the script in your Domoticz scripts folder
2. Change the IP address of the iBox controller in the script: variable **UDP_IP**
3. Add a virtual/dummy switch in Domoticz (see https://www.domoticz.com/wiki/Wemo#Creating_Dummy_Switches)
4. The ON action of the dummy switch could be set to: `script:///<script location>/milight-home.sh ON`
This action will turn on the lights of the bulbs **and** the iBox. If you only want to have the bulbs on, execute the script as follows (_put a device identifier (00 (=iBox), 07 (= RGBWW) or 08 (=RGBW)) as second last argument; specify the zone (00 or 01-04) as last argument_): `script:///<script location>/milight-home.sh ON 07 01` or `script:///<script location>/milight-home.sh ON 08 01`
5. The OFF action of the dummy switch could be set to: `script:///<script location>/milight-home.sh OFF`


### Standalone usage ###
   
The script can also be executed in standalone mode of course: 

    $ python milight-home.py ON <device> <zone> (<device> = 00, 07 or 08) (<zone> = 00, or 01-04)
    $ python milight-home.py OFF <device> <zone> (<device> = 00, 07 or 08) (<zone> = 00, or 01-04)
    $ python milight-home.py DISCO1 <device> <zone>
    $ python milight-home.py <command> <device> <zone> (see below for the list of valid <command>)

Complete command list (besides ON and OFF):

    ON/OFF/DISCO[1-9]/DISCOFASTER/DISCOSLOWER/WHITE/BRIGHT[0-25-50-75-100]/RED/GREEN/BLUE/AQUA


### Advanced usage: pass in the full 9 byte command ###

The script allows you to pass in the full 9 byte command (see http://www.limitlessled.com/dev/ for documentation). This can be useful when you want to tryout some commands or when you are debugging your setup.

    $ python milight-home.py CMD <full 9 byte command> <zone>

For example:

    $ python milight-home.py CMD "31 00 00 07 03 01 00 00 00 00" 00
