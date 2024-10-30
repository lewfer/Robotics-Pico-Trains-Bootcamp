# Sample program to use the RFID reader
from trainlib import *

# Set up the RFID reader
init_rfid()

# Loop while reading any card
while True:
    card = read_rfid()
    if card != None:
        print("Card with id", card, "found")
    sleep(0.5)
    
