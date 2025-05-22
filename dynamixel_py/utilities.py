from typing import Any
from dynamixel_sdk.robotis_def import *
from dynamixel_sdk.packet_handler import PacketHandler

class DxlUtils:

    def print_comm_hardware_error(self, pack_h_instance: PacketHandler, comm_result: Any, hardware_result: Any) -> None:
        if comm_result != COMM_SUCCESS:
            raise RuntimeError(f"\n{pack_h_instance.getTxRxResult(comm_result)} "
                               f"\nPlease check the following:"
                               f"\nIs the motor connected and powered?\n"
                               f"Is the correct servo_id entered?\n"
                               f"Is the correct baud rate set?\n"
                               )
        elif hardware_result != 0:
            raise RuntimeError(f"{pack_h_instance.getRxPacketError(hardware_result)}")