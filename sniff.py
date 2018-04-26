from scapy.all import *
import requests
import threading
import time, datetime
import signal, os
import ctypes

#modify the below URL to contact our server
url = 'http://cf43419f.ngrok.io/18748.php'

#A list of OUI IDs for companies that don't manufacture mobile devices
BLACKLIST = {'74:da:38' : 'Edimax','b8:27:eb' : 'Raspberry Pi', 
        '14:cc:20' : 'TPLink', '18:cf:5e' : 'Lite-on', '00:04:4b' : 'NVIDIA'}

PROBE_REQUEST_TYPE = 0
PROBE_REQUEST_SUBTYPE = 4

macDict = {}

def UpdateServer():
    print("Sending message to server with: %d value"%len(macDict))
    requests.post(url, data={"id":5, "num_people":len(macDict)})
    for key, val in macDict.items():
        #Remove any devices we haven't seen in a while
        #Phones are chattier than laptops/pcs, so we can do rough filtering by frequency of probe requests
        timeDelta = (datetime.datetime.now() - val).seconds
        #print(timeDelta)
        if (timeDelta > 120):
            macDict.pop(key)

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type==PROBE_REQUEST_TYPE and pkt.subtype==PROBE_REQUEST_SUBTYPE and pkt.addr2[0:8] not in BLACKLIST:
            #PrintPacket(pkt)
            dot11elt = pkt.getlayer(Dot11Elt)
            prismheader = pkt.getlayer(PrismHeader)
            rssi = ctypes.c_int32(prismheader.rssi).value
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
UpdateServer()
sniff(iface="ra0", prn=PacketHandler)
while true:
    t = threading.Timer(5.0, UpdateServer)
    t.start()

# The below lines are for local testing, not for actual packet capture
# packets = rdpcap('/Users/Sean/Desktop/4-17-capture2.pcapng')
# print("Done loading packets!")
# for packet in packets:
#     PacketHandler(packet)

