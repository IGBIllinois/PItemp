#!/usr/bin/env python3

import sys
import smbus
from optparse import OptionParser

DEVICE_BUS = 1
DEVICE_ADDR = 0x17

TEMP_REG = 0x01
LIGHT_REG_L = 0x02
LIGHT_REG_H = 0x03
STATUS_REG = 0x04
ON_BOARD_TEMP_REG = 0x05
ON_BOARD_HUMIDITY_REG = 0x06
ON_BOARD_SENSOR_ERROR = 0x07
BMP280_TEMP_REG = 0x08
BMP280_PRESSURE_REG_L = 0x09
BMP280_PRESSURE_REG_M = 0x0A
BMP280_PRESSURE_REG_H = 0x0B
BMP280_STATUS = 0x0C
HUMAN_DETECT = 0x0D

bus = smbus.SMBus(DEVICE_BUS)

aReceiveBuf = []
aReceiveBuf.append(0x00)
for i in range(TEMP_REG,HUMAN_DETECT + 1):
    aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

usage = "usage:%prog [options] arg"
parser = OptionParser(usage)

parser.add_option("--temp-external",action='store_true',help='Get External Temperature (F)');
parser.add_option("--humidity",action='store_true',help="Get Humidity (%)");
(options,args) = parser.parse_args()

if len(sys.argv) == 1:
	parser.print_help()
	quit(1)

elif (options.humidity != None):
    print("%d %%" % aReceiveBuf[ON_BOARD_HUMIDITY_REG])

elif (options.temp_external != None):
	if aReceiveBuf[STATUS_REG] & 0x01 :
		print("Off-chip temperature sensor overrange!")
	elif aReceiveBuf[STATUS_REG] & 0x02 :
		print("No external temperature sensor!")
	else :
                fahrenheit = 9.0/5.0 * aReceiveBuf[TEMP_REG] + 32
                print("%d" % fahrenheit)

'''
if aReceiveBuf[STATUS_REG] & 0x04 :
    print("Onboard brightness sensor overrange!")
elif aReceiveBuf[STATUS_REG] & 0x08 :
    print("Onboard brightness sensor failure!")
else :
    print("Current onboard sensor brightness = %d Lux" % (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L]))

print("Current onboard sensor temperature = %d Celsius" % aReceiveBuf[ON_BOARD_TEMP_REG])
print("Current onboard sensor humidity = %d %%" % aReceiveBuf[ON_BOARD_HUMIDITY_REG])

if aReceiveBuf[ON_BOARD_SENSOR_ERROR] != 0 :
    print("Onboard temperature and humidity sensor data may not be up to date!")

if aReceiveBuf[BMP280_STATUS] == 0 :
    print("Current barometer temperature = %d Celsius" % aReceiveBuf[BMP280_TEMP_REG])
    print("Current barometer pressure = %d pascal" % (aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16))
else :
    print("Onboard barometer works abnormally!")

if aReceiveBuf[HUMAN_DETECT] == 1 :
    print("Live body detected within 5 seconds!")
else:
    print("No humans detected!")
'''


