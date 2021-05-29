# Tricorder on a Raspberry pi

# Hardware:
## CPU
Raspberry Pi Zero W
https://www.adafruit.com/product/3400

## Display
2.2" 18-bit color TFT LCD
https://www.adafruit.com/product/1480

## Moire light:
NeoPixel Jewel - 7
https://www.adafruit.com/product/2860

## Sensors:
- SHT31 Temp humidity
- BMP280 Temp pressure altitude
- SI1145 Digital UV/Index/IR/Visible
- https://www.adafruit.com/product/1777

---
# Case
Several choices for a case were looked at.
- The Playmate case was just a bit too small.
- I chose the Diamond Select (a.k.a Art Asylum) for the price (about $100 on eBay) and size.
- It looks like it's nearly identical to the one used on set.
- The Master Replica (MR) one was expensive ($500) and I really couldn't find one readily but is really well constructed.
- The Marko ProBuilt, while rare, would work as well.  It's aluminum construction is much nicer than the plastic in the DS but it's expensive when I could even find one. 

- Also, the Wand company is making a replica that looks like it will be amazing!
- https://www.thewandcompany.com/star-trek-tricorder/
- But, it's too nice to tear down for the case.

# Other Resources:
- http://www.herocomm.com/SurvivingProps/Tricorders.htm
- https://memory-alpha.fandom.com/wiki/Starfleet_tricorder
- https://discuss.fleetworkshop.org/t/the-building-of-a-tos-tricorder/113/1
- https://hackaday.com/2018/03/19/building-a-tricorder-prop-worthy-of-mr-spock/
- https://www.instructables.com/Build-a-working-tricorder/


# Code
- Assets: Manage audio and video assets
- Display: Handle display modes, medical, environmental, etc.
- Indicator: Displays sensor readings
- Inputs: button inputs
- ModeTransitions: state machine for display modes and sensor modes
- Records: Archives and other records.
- Sensor: Reads sensors
- SensorArray: Collection of sensors for each mode.
- Tricorder: overall coordination and modes: demo, live, simulated.

- cd <project>
- python3 -m venv venv
- source venv/bin/activate
- pip install --upgrade pip
- pip install Pillow
- pip install pygame==1.9.4
- pip install board
- pip install adafruit-circuitpython-sht31d
- pip install adafruit-circuitpython-bmp280
- pip install AdaFruit-GPIO
- Enable I2C:  Config->Interfaces



# Operating instructions
## Button A - Operation Mode
Hitting the 'A' button advances the mode, wrapping at the end.
- E1: Environmental 1; Temp, Pressure, Humidity
- E2: Environmental 2; Temp, Pressure, Humidity, Altitude
- P: Positional; Accelerometer, Magnetometer, Proximity
- A: Audio/Visual; RGB, Light, Audio
- R: Records; Search Archival records

## Button B - Display Mode
Hitting the 'B' button advances the display mode with wrap. 
Different operation modes have different display modes
- E1: Slider, graph
- E2: text, graph
- P: text, 3D
- A: text
- R: text, video

## Button C - Command
- E1: Resets sensors
- E2: Resets sensors
- P: Resets sensors
- A: Records audio to Archive
- R: Selects next archive record

