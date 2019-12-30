#!/usr/bin/python3

import subprocess
import re
from pathlib import Path

wnic = "wlp61s0"

cmd_ap = subprocess.Popen(['nmcli -f BSSID,ACTIVE dev wifi list | awk \'$2 ~ /yes/ {print $1}\''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
ap = cmd_ap.stdout.read().decode('utf-8').strip('\n').lower()

cmd_rssi = subprocess.Popen(['cat /proc/net/wireless | grep ' + wnic + ' | cut -d " " -f 7 | head -c 3'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
rssi = cmd_rssi.stdout.read().decode('utf-8')
rssi = rssi.strip('\n')

cmd_ch = subprocess.Popen(['sudo iwlist ' + wnic + ' frequency |  grep Current | awk \'{print $5}\' | sed s/[^0-9]*//g'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
ch = cmd_ch.stdout.read().decode('utf-8')
ch = ch.strip('\n')

cmd_ht = subprocess.Popen(['sudo iw dev | grep -i ' + wnic + ' -A 10 | grep -w "width: [0-9]*" | awk \'{print $6}\''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
ht = cmd_ht.stdout.read().decode('utf-8')
ht = ht.strip('\n')

# Find name of AP
home = str(Path.home())
try:
    f = open(home + "/.config/polybar/ap_list.csv", "r")
    data = f.readlines()
    for line in data:
        line = line.strip('\n').lower()
        ap_name, mac = line.split(",")

        if ap[:16] == mac[:16]:
            ap = ap_name
            break
except IOError:
    pass
    
print(rssi + " dBm, Ch " + ch + ", " + ht + " Mhz @ " + ap)

