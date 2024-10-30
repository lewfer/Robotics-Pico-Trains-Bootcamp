# Sample program to use the 16x2 LCD display
from trainlib import *

# Set up the LCD
init_lcd()

# Show a message
write_lcd("Hello", "World")
sleep(2)

# Count numbers
for i in range(20):
    write_lcd("Counting", str(i))
    sleep(0.5)
    
# Clear the screen
write_lcd("", "")
