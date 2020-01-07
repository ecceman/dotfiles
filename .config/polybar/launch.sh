#!/bin/bash

# Kill current instances
killall -q polybar

# Wait until the processes have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

# Launch polybar for all connected monitors
if type "xrandr"; then
  for m in $(xrandr --query | grep " connected" | cut -d" " -f1); do
    polybar --reload $m &
  done
else
  polybar --reload eDP1 &
fi
