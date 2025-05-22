import time

from dynamixel_py import DxlComm, Servo

# Starting communication with U2D2 or similar device
serial = DxlComm(port="/dev/ttyUSB0")  # Eg: COM28 for windows

# Declaring a servo object
servo1 = Servo(servo_id=1, control_table="XL330")

# Disabling torque for a single servo
servo1.torque_enabled(is_enabled=False)

try:
    while True:
        print(servo1.get_position())
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stopping program")
