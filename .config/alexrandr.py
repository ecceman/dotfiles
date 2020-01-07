#!/usr/bin/python3

import subprocess
import logging
import time


def main():
    internal_display = "eDP1"
    external_display = ""
    external_display_connected = False

    while True:
        xrandr_get_displays_cmd = 'xrandr | grep -w "connected" | awk \'{print $1}\''
        xrandr_output = subprocess.Popen([xrandr_get_displays_cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        xrandr_output = xrandr_output.stdout.read().decode('utf-8').splitlines()

        if len(xrandr_output) == 1 and external_display_connected is True: # External display is disconnected
            xrandr_set_displays_cmd = 'xrandr --auto'
            external_display_connected = False
            logging.info('External display disconnected. Running ' + xrandr_set_displays_cmd)
            print(xrandr_set_displays_cmd)
            exec_display_change(xrandr_set_displays_cmd)
        elif len(xrandr_output) > 1 and external_display_connected is False: # External monitor is connected
            for _ in xrandr_output:
                if _ != internal_display:
                    external_display = _
                    break
            xrandr_set_displays_cmd = 'xrandr --output ' + external_display + ' --above ' + internal_display + ' --auto'
            external_display_connected = True
            logging.info('External monitor connected. Running ' + xrandr_set_displays_cmd)
            print(xrandr_set_displays_cmd)
            exec_display_change(xrandr_set_displays_cmd)

        time.sleep(4)


def exec_display_change(xrandr_set_cmd):
    tmp_output = subprocess.Popen([xrandr_set_cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    tmp_output = subprocess.Popen(['~/.config/polybar/launch.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    tmp_output = subprocess.Popen(['feh --bg-scale ~/Pictures/debian.jpg'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)


if __name__ == '__main__':
    main()
