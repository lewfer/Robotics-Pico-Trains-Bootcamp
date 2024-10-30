# Sample program to use the DC motors
from trainlib import *

# Set up the motor
init_motor()

# Move forwards, backwards then stop
motor_forward(0, 100)
sleep(2)
motor_backward(0, 50)
sleep(3)
motor_stop(0)
