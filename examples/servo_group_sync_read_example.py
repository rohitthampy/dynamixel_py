import time
from dynamixel_py import DxlComm, Servo, ServoGroup

serial = DxlComm(port="/dev/ttyUSB0")

servo1 = Servo(servo_id=1, control_table="XL330")
servo2 = Servo(servo_id=12, control_table="XL330")
servo3 = Servo(servo_id=15, control_table="XL330")

servo_group = ServoGroup()
servo_group.add_servos([servo1, servo2, servo3])

print(servo_group.get_total_servos())

servo_group.sync_torques_enabled(False)

while True:
    try:
        print(servo_group.sync_get_positions())
    except KeyboardInterrupt:
        print("Stopping program")
