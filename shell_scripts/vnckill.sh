#!/bin/sh
# kills a vnc session if the VNC_DISPLAY environment variable is set

VNCSERVER=/usr/bin/vncserver

# check that the VNC_DISPLAY environment variable is set
if [ -z "$VNC_DISPLAY" ]; then
	echo "VNC_DISPLAY environment variable unset, did you use the vnc command to start your vnc server?"
	exit 1
fi

echo Killing VNC display $VNC_DISPLAY
$VNCSERVER -kill :$VNC_DISPLAY