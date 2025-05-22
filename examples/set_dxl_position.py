import time

from dynamixel_py import DxlComm, Servo

# Starting communication with U2D2 or similar device
serial = DxlComm(port="/dev/ttyUSB0")  # Eg: COM28 for windows

# Declaring a servo object
servo1 = Servo(servo_id=1, control_table="XL330")

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

servo1.set_position(180)
time.sleep(1)
