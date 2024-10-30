# Library of functions for GIC train activity

from time import sleep
import network
from time import sleep
import urequests as requests
import gc
import json

control_centre_url = "http://192.168.1.10:8000/"

# Global objects set with _init functions called
motor_board = None
reader = None
i2c = None
lcd = None

# Motors
# -------------------------------------------------------------------

# Initialise the motor driver
def init_motor():
    global motor_board
    from SimplyRobotics import KitronikSimplyRobotics    
    motor_board = KitronikSimplyRobotics()
    
def motor_forward(motor, speed):
    motor_board.motors[motor].on("f", 100)

def motor_backward(motor, speed):
    motor_board.motors[motor].on("r", 100)
    
def motor_stop(motor):
    motor_board.motors[motor].off()
    

# RFID reader
# -------------------------------------------------------------------

# Initialise the RFID sensor
def init_rfid():
    global reader
    from mfrc522 import MFRC522
    reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
    
# Read id from tag, if present
def read_rfid():
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            return card
    return None

# 16x2 LCD display
# -------------------------------------------------------------------

# Initialise the LCD 
def init_lcd():
    global i2c, lcd
    from lcd_api import LcdApi
    from machine import I2C, Pin
    from pico_i2c_lcd import I2cLcd
    i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
    x = i2c.scan()
    print(x)
    I2C_ADDR = i2c.scan()[0]
    print(I2C_ADDR)
    lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
    lcd.blink_cursor_off()
    lcd.backlight_on()
    lcd.hide_cursor()
    
# Write text to the lcd display
def write_lcd(line1, line2):
    lcd.clear()
    lcd.putstr(line1 +"\n")
    lcd.putstr(line2)


# Control centre
# -------------------------------------------------------------------

# Connect to wifi, retrying until success
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print("WiFi connected", wlan.ifconfig())

# Report location of train with given id
def report(id, location):
    #print("Sending to control centre...")
    url = control_centre_url + f"/report?id={id}&location={location}"
    
    response = requests.get(url)
    response_code = response.status_code
    response_content = response.content
    if response_code==200:
        return json.loads(response_content.decode('utf-8'))
    else:
        print('Response code: ', response_code)
        return None

# Get info screen for location
def info(location):
    #print("Sending to control centre...")
    url = control_centre_url + f"/info?location={location}"
    
    response = requests.get(url)
    response_code = response.status_code
    response_content = response.content
    if response_code==200:
        return json.loads(response_content.decode('utf-8'))
    else:
        print('Response code: ', response_code)
        return None

# Get next action for train with given id
def action(id):
    #print("Sending to control centre...")
    url = control_centre_url + f"/action?id={id}"
    
    response = requests.get(url)
    response_code = response.status_code
    response_content = response.content
    if response_code==200:
        return json.loads(response_content.decode('utf-8'))
    else:
        print('Response code: ', response_code)
        return None
    
