#!/bin/bash
# fixes the permissions for a directory meant to be served via Apache/httpd
PWD=`pwd`
DIRECTORY=$PWD"/"$1"/"
echo "Fixing permissions in "$DIRECTORY
echo "Requires sudo privileges"

echo "Chmod-ing directories to 775 and setting the setgid bit"
sudo find $DIRECTORY -type d -exec chmod 775 '{}' \;
sudo find $DIRECTORY -type d -exec chmod g+s '{}' \;

echo "Chmod-ing files to 664"
sudo find $DIRECTORY -type f -exec chmod 664 '{}' \;

echo "Setting owner.group to root.developers for all directories and files"
sudo chown -R root.developers $DIRECTORY
