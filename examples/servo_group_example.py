import time
import random
from dynamixel_py import DxlComm, Servo, ServoGroup

serial = DxlComm(port="/dev/ttyUSB0")

servo1 = Servo(servo_id=1, control_table="XL330")
servo2 = Servo(servo_id=12, control_table="XL330")
servo3 = Servo(servo_id=15, control_table="XL330")

servo_group = ServoGroup()
servo_group.add_servos([servo1, servo2, servo3])

print(servo_group.get_total_servos())

servo_group.sync_torques_enabled(True)

print(servo_group.sync_get_positions())

servo_group.sync_set_positions([180, 180, 180])
time.sleep(0.5)

# Sends the servos to random positions between 0 and 350 degrees
for i in range(10):
    servo_group.sync_set_positions(
        [random.randint(0, 350), random.randint(0, 350), random.randint(0, 350)]
    )
    time.sleep(0.5)
    print(servo_group.sync_get_positions())

servo_group.sync_set_positions([180, 180, 180])
time.sleep(0.5)
