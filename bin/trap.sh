#!/bin/bash

TEMPERATURE=`/home/pi/alert/bin/read_sensors.py --temp-external`
TEMP_LOW=20
#TEMP_HIGH=82
TEMP_HIGH=60
LAST_TRAP="/home/pi/alert/last_sent"

subject="ERML 336 Temperature"
from="dslater@igb.illinois.edu"
to="dslater@igb.illinois.edu"

echo "Temp is $TEMPERATURE"

CURRENT_TIME=$(date +"%s")
PREVIOUS_TIME=`cat /home/pi/alert/last_sent`
TIME_DIFF=$(( $CURRENT_TIME - $PREVIOUS_TIME ))
echo "DIFF: $TIME_DIFF"
if [ $TIME_DIFF -gt 3600 ]
then
	if [ $TEMPERATURE -gt $TEMP_HIGH ]
	then
	
		echo "Temperature High: Current Temp: $TEMPERATURE, Above $TEMP_HIGH"
		snmptrap -v 2c -c public 128.174.124.86:162 'Test'  1.3.6.1.4.1.8072.2.3.0.1 1.3.6.1.4.1.8072.2.3.2.1 s "Temp Too High: $TEMPERATURE F, Above $TEMP_HIGH" \
			SNMPv2-MIB::sysLocation.0 s "ERML 336"
		#body="Temperature: $TEMPERATURE, Above $TEMP_HIGH\n"	
		#echo -e "Subject:${subject}\nFrom:${from}\n${body}" | sendmail ${to}
		echo $CURRENT_TIME > $LAST_TRAP
		exit 1

	elif [ $TEMPERATURE -lt $TEMP_LOW ]
	then
		echo "Temperature Low: Current Temp: $TEMPERATURE, Below $TEMP_LOW"
		snmptrap -v 2c -c public 128.174.124.86:162 'Test'  1.3.6..4.1.8072.2.3.0.1 1.3.6.1.4.1.8072.2.3.2.1 s "Temp Too Low: $TEMPERATURE F, Below $TEMP_LOW" \
        		SNMPv2-MIB::sysLocation.0 s "ERML 336"
		echo $CURRENT_TIME > $LAST_TRAP
		exit 1

	fi
fi

