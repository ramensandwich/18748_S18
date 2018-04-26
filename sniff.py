from scapy.all import *
import requests
import threading
import time
import signal, os

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
    for key in macDict:
        #Remove any devices we haven't seen in a while
        if (macDict[key] - time.clock() > 30):
            macDict.pop(key)

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type==PROBE_REQUEST_TYPE and pkt.subtype==PROBE_REQUEST_SUBTYPE and pkt.addr2[0:8] not in BLACKLIST:
            PrintPacket(pkt)
            if(pkt.addr2 not in macDict):
                macDict[pkt.addr2] = time.clock()



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

