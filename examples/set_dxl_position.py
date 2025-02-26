import time

from servos.XL330 import XL330Comm, XL330Ctrl

# Starting communication for Dynamixel servo
serial = XL330Comm(port="COM28")

# Declaring a servo object
servo1 = XL330Ctrl(servo_id=8)
# Adding servo to start communication
serial.add_servo(servo=servo1)

# Enabling torque for a single servo
servo1.torque_enabled(is_enabled=True)

count_1 = 0
servo1.set_position(count_1)
time.sleep(1)

while count_1 < 359:
    count_1 += 1
    servo1.set_position(count_1)

while count_1 > 0:
    count_1 -= 1
    servo1.set_position(count_1)
