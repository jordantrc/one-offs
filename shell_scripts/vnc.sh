#!/bin/sh
# sets a display id based on the uid of the user
# echoes the port number to use when connecting using xrdp

UID=`id -u`
BASE_ID=16777216
DISPLAYID=`expr $UID - $BASE_ID`
VNCSERVER=/usr/bin/vncserver
GEOMETRY=1280x1024

PORT=`expr $DISPLAYID + 5900`

if [ -z "$1" ]; then
	$VNCSERVER -geometry $GEOMETRY :$DISPLAYID
	echo Your VNC port number is $PORT
	exit 0
elif [ $1 = "-kill" ]; then
	echo Killing VNC display $DISPLAYID
	$VNCSERVER -kill :$DISPLAYID
fi