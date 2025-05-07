import time

from dynamixel_py import DxlComm, DxlCtrl

# Starting communication for Dynamixel servo
serial = DxlComm(port="/dev/ttyUSB0") # Eg: COM28 for windows

# Declaring a servo object
servo1 = DxlCtrl(servo_id=1, control_table="XL330")

# # # Adding servo to start communication
serial.add_servo(servo=servo1)
#
# # Disabling torque for a single servo
servo1.torque_enabled(is_enabled=False)

try:
    while True:
        print(servo1.get_position())
        time.sleep(0.1)


except KeyboardInterrupt:
    print("Stopping program")
