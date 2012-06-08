#!/bin/sh
#
# This script is called during the GL setup, its executed only one time, and basically
# execute Tor with the hidden service configured, get the HS hostname.onion and copy it
# in the configuration file.
#
# is not so clean, and maybe a python script that interact RW with config file is better :)
#
# this is one of the file added for GL-virtual package

GL01="/home/globaleaks/GL-01/"
HSfile="/home/globaleaks/HS/hostname"
cd $GL01

echo "Starting Hidden Service for the first time"
/etc/init.d/tor start
sleep 1

if [ ! -e "$HSfile" ]; then
	echo "[-] Unable to startup hidden service: something wrong in your network, required by hand debug"
	return 1
fi

hiddenservice=`cat $HSfile` 
echo "[+] started hidden service with name $hiddenservice pointing to 172.16.254.2:8000"
echo "[+] changing configuration file with hidden service $hiddenservice"
cat $GL01/globaleaks/globaleaks.conf | sed -es/hsurl\ =.*/hsurl\ =\ $hiddenservice/ > /tmp/globaleaks.conf-hs
cp /tmp/globaleaks.conf-hs $GL01/globaleaks/globaleaks.conf

sleep 1
return 0

