from scapy.all import *
import requests
import threading
import time, datetime
import signal, os
import ctypes
import hashlib

#modify the below URL to contact our server
url = 'http://3e250a62.ngrok.io/18748.php'

#A list of OUI IDs for companies that don't manufacture mobile devices
BLACKLIST = {'74:da:38' : 'Edimax','b8:27:eb' : 'Raspberry Pi', 
        '14:cc:20' : 'TPLink', '18:cf:5e' : 'Lite-on', '00:04:4b' : 'NVIDIA'}

PROBE_REQUEST_TYPE = 0
PROBE_REQUEST_SUBTYPE = 4

macDict = {}

LOG = open("logged.txt", "w")

def UpdateServer():
    print("Sending message to server with: %d value"%len(macDict))

    #We don't want to transmit actual device MAC addresses, so we'll transmit a hash instead
    deviceHashes = []
    for MACaddress in macDict.keys():
        deviceHashes.append(hashlib.md5(MACaddress).digest())

    macString = ''.join(x + ',' for x in macDict.keys())[0:-1]

    print(macString)


    try:
        requests.post(url, data={"locationID":"ABP", "macs":macString})
    except:
        print("Error sending to server!")
    

    LOG.write(str(len(macDict)) + ",")
    LOG.flush()
    
    for key, val in macDict.items():
        #Remove any devices we haven't seen in a while
        #Phones are chattier than laptops/pcs, so we can do rough filtering by frequency of probe requests
        timeDelta = (datetime.datetime.now() - val).seconds
        #print(timeDelta)
        if (timeDelta > 120):
            macDict.pop(key)
    t = threading.Timer(10.0, UpdateServer)
    t.start()


def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type==PROBE_REQUEST_TYPE and pkt.subtype==PROBE_REQUEST_SUBTYPE and pkt.addr2[0:8] not in BLACKLIST:
            #PrintPacket(pkt)
            dot11elt = pkt.getlayer(Dot11Elt)
            prismheader = pkt.getlayer(PrismHeader)
            rssi = ctypes.c_int32(prismheader.rssi).value
            #TODO: Investigate why 71 is so prevalent as an RSSI value
            print("rssi: " + str(rssi))
            if (rssi <= -70): return
            while dot11elt:
                if (dot11elt.ID == 221):
                    vendInfo = ''.join(["%02X" % ord(x) for x in dot11elt.info]).strip()
                    #print(vendInfo[0:6])
                    if(vendInfo[0:6] == "0050F2"):
                        macDict[pkt.addr2] = datetime.datetime.now()
                        print("Device MAC: " + str(pkt.addr2))
                        return
                dot11elt = dot11elt.payload.getlayer(Dot11Elt)

def PrintPacket(pkt):
    try:
        extra = pkt.notdecoded
    except:
        extra = None
    if extra != None:
        signal_strength = -(256-ord(extra[-4:-3]))
    else:
        signal_strength = -100
        print("No signal strength found")
    print "Target: %s Source: %s SSID: %s RSSI: %d"%(pkt.addr3, pkt.addr2, pkt.getlayer(Dot11ProbeReq).info, signal_strength)
#    pkt.show()
    dot11elt = pkt.getlayer(Dot11Elt)
    while dot11elt:
        if (dot11elt.ID == 221):
            print("Vendor specific!")
            print(len(dot11elt.info))
            vendInfo = ''.join( [ "%02X " % ord(x) for x in dot11elt.info ]).strip()
            print(vendInfo)
        print dot11elt.ID #, dot11elt.info
        dot11elt = dot11elt.payload.getlayer(Dot11Elt)

t = threading.Timer(10.0, UpdateServer)
t.start()

#IMPORTANT: sniff by default stores all packets it catches. This is bad for our embedded system
sniff(iface="ra0", prn=PacketHandler, store=0)
