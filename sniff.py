from scapy.all import *
import requests
import threading
import time

#modify the below URL to contact our server
url = 'http://a70f6c06.ngrok.io/18748.php'



PROBE_REQUEST_TYPE = 0
PROBE_REQUEST_SUBTYPE = 4

macDict = {}

def UpdateServer():
    print("Sending message to server with: %d value"%len(macDict))
    requests.post(url, data={"id":5, "num_people":len(macDict)})
    t = threading.Timer(10.0, UpdateServer)
    t.start()

def PacketHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type==PROBE_REQUEST_TYPE and pkt.subtype==PROBE_REQUEST_SUBTYPE:
            PrintPacket(pkt)
            if(pkt.addr2 not in macDict):
                macDict[pkt.addr2] = 1


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

#TODO: Change time value back to 30 or 60. 10 is for testing purposes
#t = threading.Timer(10.0, UpdateServer)
#t.start()
UpdateServer()
sniff(iface="ra0", prn=PacketHandler)

