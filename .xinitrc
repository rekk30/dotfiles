xrdb /home/admin/.Xresources

setxkbmap "us,ru" ",winkeys" "grp:alt_shift_toggle"
xset r rate 160 55
if [ `xinput --list | grep "Razer Razer BlackWidow Ultimate" | wc -l` -gt 0 ]
then
    xinput --disable "ELAN1300:00 04F3:3059 Touchpad"
fi

export ICAROOT="/opt/Citrix/ICAClient/"
pulseaudio --daemonize
# systemctl --user start mpd.service
exec i3


