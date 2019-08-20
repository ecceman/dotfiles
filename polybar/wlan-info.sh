#!/bin/sh

AP="$(nmcli -f BSSID,ACTIVE dev wifi list | awk '$2 ~ /yes/ {print $1}')"
RSSI="$(cat /proc/net/wireless | grep wlp4s0 | cut -d " " -f 7 | head -c 3)"
CH="$(sudo iwlist wlp4s0 frequency |  grep Current | awk '{print substr($5,0,2)}')"

# Map AP Mac-address to AP Name (if any)
case $AP in
	FC:EC:DA:B2:57:DA)
		AP=Unifi_1
		;;
	F0:9F:C2:3B:CA:7F)
		AP=Unifi_2
		;;
	*)
		AP=$AP
esac

echo "${RSSI}dBm @ Ch ${CH} @ ${AP}"
