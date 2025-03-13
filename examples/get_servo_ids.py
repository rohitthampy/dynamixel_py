from dynamixel_py.servos.XL330 import XL330Comm

serial = XL330Comm(port="COM28")

servo_ids = serial.get_servo_ids()

print(servo_ids)
