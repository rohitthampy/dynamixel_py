## Acknowledgement

Most of the source code and architecture used in this project was adapted from the [PyDynamixel_v2](https://github.com/TauraBots/PyDynamixel_v2/tree/more_robust) library made by the amazing members of [TauraBots](https://github.com/TauraBots).

## About this library

This library wraps the [dynamixel_sdk](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/overview/#dynamixel-sdk) 
to hide its complexity and attempts to expose its features in a more user-friendly manner.

It has three classes. 
- `DxlComm` is responsible for opening and starting a communication port like USB.
- `Servo` is responsible for controlling dynamixel motors. You can use it for things such as getting the position of the servo, sending to to a goal position etc.
- `ServoGroup` is responsible for sending commands and receiving data from servos with the same control table and protocol simultaneously.

## Installing

### Simple install
The quickest and easiest way of installing this library is through pip.
Run the command `pip install dynamixel-py`

### Install from source
1) Clone this repository using `git clone https://github.com/rohitthampy/dynamixel_py.git`
2) Create a virtual environment and `pip install dynamixel-sdk`
3) Create your python project at the root of this repository.
4) Have a look at the examples for inspiration.

## Usage Examples
### Examples for controlling one motor at a time
- Getting position data from a servo
```python
import time

from dynamixel_py import DxlComm, Servo

# Starting communication with U2D2 or similar device
serial = DxlComm(port="/dev/ttyUSB0") # Eg: COM28 for windows

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
```


- Setting the position of a servo

```python
import time

from dynamixel_py import DxlComm, Servo

# Starting communication with U2D2 or similar device
serial = DxlComm(port="/dev/ttyUSB0") # Eg: COM28 for windows

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
```
- Controlling motors of Protocol 1.0 and Protocol 2.0

```python
import time

from dynamixel_py import DxlComm, Servo

# Starting communication with U2D2 or similar device
serial = DxlComm(port="/dev/ttyUSB0", baud_rate=1000000) # Eg: COM28 for windows

# Declaring servo objects
# By default, the baud rate for the XC330 is 57600, this was changed to 1000000 to work with the AX12
servo1 = Servo(servo_id=1, control_table="XC330") # Using the default protocol version which is 2

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

```

### Examples using sync read/write to control motor simultaneously

- Using sync read to read positions of multiple motors
```python
from dynamixel_py import DxlComm, Servo, ServoGroup

serial = DxlComm(port="/dev/ttyUSB0")

servo1 = Servo(servo_id=1, control_table="XL330")
servo2 = Servo(servo_id=12, control_table="XL330")
servo3 = Servo(servo_id=15, control_table="XL330")

servo_group = ServoGroup()
servo_group.add_servos([servo1, servo2, servo3])

print(servo_group.get_total_servos())

servo_group.sync_torques_enabled(False)

try:
    while True:
        print(servo_group.sync_get_positions())

except KeyboardInterrupt:
    print("Stopping program")

```

- Using sync write to simultaneously control multiple servos

```python
import time
from dynamixel_py import DxlComm, Servo, ServoGroup

serial = DxlComm(port="/dev/ttyUSB0")

servo1 = Servo(servo_id=1, control_table="XL330")
servo2 = Servo(servo_id=12, control_table="XL330")
servo3 = Servo(servo_id=15, control_table="XL330")

servo_group = ServoGroup()
servo_group.add_servos([servo1, servo2, servo3])

print(servo_group.get_total_servos())

servo_group.sync_torques_enabled(True)

servo_group.sync_set_positions([30, 45, 90])
time.sleep(1)


servo_group.remove_servos([servo1, servo2, servo3])
print(servo_group.get_total_servos())

```
- Using sync read and write together
```python
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
    servo_group.sync_set_positions([random.randint(0, 350),
                                    random.randint(0, 350),
                                    random.randint(0, 350)])
    time.sleep(0.5)
    print(servo_group.sync_get_positions())

servo_group.sync_set_positions([180, 180, 180])
time.sleep(0.5)
```