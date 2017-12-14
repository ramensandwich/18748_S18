ifconfig ra0 up
sleep 1
iwconfig ra0 mode monitor channel 7
sleep 1
python /root/Documents/18748_S18/sniff.py
