if [[ ! $DISPLAY && $XDG_VTNR -le 3 ]]; then
	exec startx
fi
