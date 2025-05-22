import time

from dynamixel_py import DxlComm, Servo

# Starting communication with U2D2 or similar device
serial = DxlComm(port="/dev/ttyUSB0", baud_rate=1000000)  # Eg: COM28 for windows

# Declaring servo objects
# By default, the baud rate for the XC330 is 57600, this was changed to 1000000 to work with the AX12
servo1 = Servo(
    servo_id=1, control_table="XC330"
)  # Using the default protocol version which is 2

servo2 = Servo(servo_id=11, control_table="AX12", protocol_version=1)

# Enabling torque for both servos
servo1.torque_enabled(is_enabled=True)
servo2.torque_enabled(is_enabled=True)

count_1 = 0
servo1.set_position(count_1)
time.sleep(1)

while count_1 < 359:
    count_1 += 1
    servo1.set_position(count_1)
    servo2.set_position(count_1)

while count_1 > 0:
    count_1 -= 1
    servo1.set_position(count_1)
    servo2.set_position(count_1)

servo1.set_position(180)
servo2.set_position(180)
time.sleep(1)
