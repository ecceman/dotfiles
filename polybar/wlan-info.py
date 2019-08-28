#!/usr/bin/python3

import subprocess
import re
from pathlib import Path

cmd_ap = subprocess.Popen(['nmcli -f BSSID,ACTIVE dev wifi list | awk \'$2 ~ /yes/ {print $1}\''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
ap = cmd_ap.stdout.read().decode('utf-8').strip('\n').lower()

cmd_rssi = subprocess.Popen(['cat /proc/net/wireless | grep wlp4s0 | cut -d " " -f 7 | head -c 3'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
rssi = cmd_rssi.stdout.read().decode('utf-8')

cmd_ch = subprocess.Popen(['sudo iwlist wlp4s0 frequency |  grep Current | awk \'{print substr($5,0,2)}\''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
ch = cmd_ch.stdout.read().decode('utf-8')
ch = re.sub("[^0-9]", "", ch)

cmd_ht = subprocess.Popen(['sudo iw dev | grep -i wlp4s0 -A 10 | grep -w "width: [0-9]*" | awk \'{print $6}\''], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
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
