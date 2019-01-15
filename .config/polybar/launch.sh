#!/usr/bin/env sh

# Terminate already running bar instances
killall -q polybar

# Wait until the processes have been shut down
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

polybar advance -c ~/.config/polybar/advance &
sleep 0.1
polybar-msg cmd toggle
sleep 1
polybar main &