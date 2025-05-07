from dynamixel_py import DxlComm

serial = DxlComm(port="COM28")

servo_ids = serial.get_servo_ids()

print(servo_ids)
