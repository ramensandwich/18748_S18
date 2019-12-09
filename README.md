# 18748 Spring 2018 Group 15 Presence detection

### Problem introduction
People counting is an unsolved problem.  Current solutions range from primitive break-beam sensors to cameras backed with advanced computer vision algorithms.  We propose the monitoring of wireless internet traffic to determine the number of people in a given space. We believe this solution will be superior to existing ones because it *reduces cost* while achieving *higher accuracy* than current solutions.  We achieve lower setup costs by piggybacking off of existing wireless internet infrastructure, and achieve higher accuracy by precisely filtering and counting relevant devices.

### Testing setup
To set our theory, we utilize a network of Raspberry Pis connected to a central server.

## Creating the kali linux images on Mac OS X

First, download the official Raspberry Pi 3 Kali Linux image off of the [official Kali Linux website](https://docs.kali.org/kali-on-arm/install-kali-linux-arm-raspberry-pi)

Once you have an 8Gb (preferably larger) sd card inserted into your computer, find out which drive is the sd card with the following command:
```df -h```

**note: name_of_sd_card_partition and name_of_sd_card are not necessarily the same.** So if your sd card partition is called /dev/disk3s1, then the sd card may be called /dev/disk3

Once you've found the diskname of the sd card, run:
```sudo diskutil unmount /dev/name_of_sd_card_partition```

Lastly, to put the image on the sd card:
```
sudo dd if=path_to_kali.img of=/dev/name_of_sd_card bs=20m
```
Adjust the bs parameter according to the speed of your sd card. This step can take more than 15 minutes. Using ctrl+t shows the imaging progress.

## Setting up the AC600 wireless dongle

Sometimes Kali Linux does not have the necessary drivers to work with the AC600 because there are two chipsets for the same product. If plug-and-play does not work, then follow [these instructions](https://medium.com/@honsontran/installing-tp-link-archer-t2uh-ac600-on-vmware-for-kali-linux-4fa2db52cd69) 


## Starting the sniffer

On the command line, input the following, replacing "wlan-name" with the name of your wireless interface.
```
ifconfig wlan-name down
iwconfig wlan-name mode monitor
ifconfig wlan-name up
```

