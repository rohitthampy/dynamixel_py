from dynamixel_sdk import *
from .dynamixel_control_tables import *
from serial import SerialException
from typing import Any
from math import pi

PORT_HANDLER = None
DEFAULT_PROTOCOL_VERSION = 2
HOMING_OFFSET = 0


class DxlComm:

    def __init__(self, port: str = None, baud_rate: int = 57600):

        self.port = port
        self.baud_rate = baud_rate

        self.port_handler = PortHandler(port)
        global PORT_HANDLER
        PORT_HANDLER = self.port_handler

        try:
            self.port_handler.openPort()
        except SerialException as e:
            print(e)
            raise RuntimeError(e)
        else:
            print(f"Succeeded to open port {self.port}")

        try:
            self.set_comm_baud_rate()
        except SerialException as e:
            print(e)
            raise RuntimeError(e)
        else:
            print(f"Succeeded to set baud rate: {self.baud_rate}")

    def set_comm_baud_rate(self):
        self.port_handler.setBaudRate(baudrate=self.baud_rate)

    def __del__(self):
        self.port_handler.closePort()


class Servo:

    def __init__(self, servo_id: int, control_table: str, protocol_version: int = DEFAULT_PROTOCOL_VERSION):

        self.servo_id = servo_id
        self.port_handler = PORT_HANDLER

        self.protocol_version = protocol_version
        global DEFAULT_PROTOCOL_VERSION
        DEFAULT_PROTOCOL_VERSION = self.protocol_version

        self.packet_handler = PacketHandler(self.protocol_version)

        self.control_table = None
        self.middle_pos_val = 2048.0
        self.goal_pos = None
        self.is_torque_enabled = False

        if self.protocol_version not in control_tables:
            raise ValueError(f"Unsupported protocol version: {self.protocol_version}")

        valid_tables = control_tables[self.protocol_version]

        if control_table not in valid_tables:
            raise ValueError(
                f"Invalid control table {control_table} for protocol version {self.protocol_version}"
                f"\nValid options are: {list(valid_tables.keys())}"
            )
        print(f"Using control table {control_table} for protocol version {self.protocol_version}")

        if control_table == "AX12":
            print("Changing middle position value to 512")
            self._set_middle_pos_val(512.0)
        self.control_table = valid_tables[control_table]

    def _set_middle_pos_val(self, middle_value):
        self.middle_pos_val = middle_value

    def set_homing_offset(self, angle_offset: float = HOMING_OFFSET, radian: bool = False):
        if self.protocol_version == 1:
            raise RuntimeError(f"set_homing_offset is not available in {self.protocol_version}")
        if self.is_torque_enabled:
            raise ValueError("Torque must be disabled before setting homing offset")
        if radian:
            if -pi/2 <= angle_offset <= pi/2:
                homing_pos = int(self.middle_pos_val * angle_offset / pi)
            else:
                raise ValueError("Homing offset should be between -1.57 and 1.57 radians")
        else:
            if -90 <= angle_offset <= 90:
                homing_pos = int(self.middle_pos_val * angle_offset / 180)
            else:
                raise ValueError("Homing offset should be between -90 and 90 degrees")
        dxl_comm_result, dxl_error = self.packet_handler.write4ByteTxRx(self.port_handler,self.servo_id,
                                                                        self.control_table.ADDR_HOMING_OFFSET, homing_pos)
        self._print_comm_error_result(dxl_comm_result, dxl_error)
        print(f"Homing offset for servo with id {self.servo_id} is set to: {angle_offset}")


    def torque_enabled(self, is_enabled: bool = False) -> None:
        dxl_comm_result, dxl_error = self.packet_handler.write1ByteTxRx(self.port_handler, self.servo_id,
                                                                        self.control_table.ADDR_TORQUE_ENABLE, is_enabled)

        self._print_comm_error_result(dxl_comm_result, dxl_error)
        print(f"Torque for servo with id {self.servo_id} is set to: {is_enabled}")
        self.is_torque_enabled = is_enabled


    def get_position(self, radian: bool = False) -> float:
        if self.protocol_version == 1:
            reg_data, dxl_comm_result, dxl_error = self.packet_handler.read2ByteTxRx(self.port_handler, self.servo_id,
                                                                                     self.control_table.ADDR_PRESENT_POSITION)
        else:
            reg_data, dxl_comm_result, dxl_error = self.packet_handler.read4ByteTxRx(self.port_handler, self.servo_id,
                                                                                 self.control_table.ADDR_PRESENT_POSITION)
        self._print_comm_error_result(dxl_comm_result, dxl_error)

        if radian:
            angle = pi*float(reg_data)/self.middle_pos_val
        else:
            angle = 180*float(reg_data)/self.middle_pos_val
        return angle


    def _set_goal_pos(self, angle: float, radian: bool = False) -> None:
        if radian:
            self.goal_pos = int(self.middle_pos_val * angle / pi)
        else:
            self.goal_pos = int(self.middle_pos_val * angle / 180)


    def set_position(self, goal_pos, radian=False) -> None:

        self._set_goal_pos(angle=goal_pos, radian=radian)

        if self.protocol_version == 1:
            dxl_comm_result, dxl_error = self.packet_handler.write2ByteTxRx(self.port_handler, self.servo_id,
                                                                            self.control_table.ADDR_GOAL_POSITION,
                                                                            self.goal_pos)

        else:
            dxl_comm_result, dxl_error = self.packet_handler.write4ByteTxRx(self.port_handler, self.servo_id,
                                                                        self.control_table.ADDR_GOAL_POSITION,
                                                                        self.goal_pos)

        self._print_comm_error_result(dxl_comm_result, dxl_error)


    def _print_comm_error_result(self, comm_result: Any, error: Any) -> None:
        if comm_result != COMM_SUCCESS:
            print("Please check the following:\n"
                  "Is the motor connected and powered?\n"
                  "Is the correct servo_id entered?\n"
                  "Is the correct baud rate set?\n")
            raise RuntimeError(f"\n{self.packet_handler.getTxRxResult(comm_result)}")
        elif error != 0:
            raise RuntimeError(f"{self.packet_handler.getRxPacketError(error)}")
