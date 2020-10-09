# PItemp

[![Build Status](https://www.travis-ci.com/IGBIllinois/PItemp.svg?branch=main)](https://www.travis-ci.com/IGBIllinois/PItemp)

Raspberry Pi Temperature Probe

* Works on Raspberry Pi 3/4
* Uses Raspbian
* Alert for temperature and humidity

## SNMP Probes
* Add the following to /etc/snmp/snmpd.conf
```
extend external_temp /usr/local/PItemp/bin/get_temp.sh
```
* ON snmp server.  Create a high threshold probe using the variable
```
NET-SNMP-EXTEND-MIB::nsExtendOutput1Line."external_temp"
```
* Set the threshold to a temperature value in Fehrenheit

