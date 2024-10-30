from mfrc522 import MFRC522
import utime
import network
from time import sleep
import urequests as requests

ssid = 'LCM2G'
password = 'htmbwsptbwy130'


reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
 
print("Bring TAG closer...")
print("")

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    sleep(1)
print("WiFi connected", wlan.ifconfig())
    
def report(id, location):
    print("Sending to control centre...")
    url = f"http://192.168.1.10:8000/report?id={id}&location={location}"
    print(url)
    #url = "http://www.thinkcreatelearn.co.uk"

    response = requests.get(url)
    #response = requests.get("http://www.google.com")
    response_code = response.status_code
    response_content = response.content
    print('Response code: ', response_code)
    print('Response content:', response_content)

lastuid = ""
while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            if uid!=lastuid:
                lastuid = uid
                card = int.from_bytes(bytes(uid),"little",False)
                print("CARD ID: "+str(card))
                report(card, "SignalA")
utime.sleep_ms(500) 
