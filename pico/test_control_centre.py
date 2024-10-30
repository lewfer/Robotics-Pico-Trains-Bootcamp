# Sample program to use the control centre
from trainlib import *

# Connect to WiFi
connect_wifi("ssid", "password")

# Report that an RFID tag has registered at LocationA
res = report(123, "LocationA")
print("\nReported:", res)

# Get information about last locations of tags
res = info("TownCentre")
print("\nInfo:", res)

# Get next action for train with given id
res = action(123)
print("\nNext action:", res)
