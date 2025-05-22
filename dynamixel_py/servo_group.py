from .dynamixel_manager import *
from typing import Union
from dynamixel_sdk import GroupSyncRead, GroupSyncWrite
from .utilities import DxlUtils

utils = DxlUtils()

class ServoGroup:
    def __init__(self):
        self.servos: dict[int, Servo] = {}
        self.total_servos = 0

    def _add_servo(self, servo: Servo):
        if servo.servo_id in self.servos:
            raise ValueError(f"Servo with id {servo.servo_id} already exists.")

        else:
            self.servos[servo.servo_id] = servo
            print(f"Added servo with id {servo.servo_id}")
            self.total_servos += 1

    def add_servos(self, servo_list: Union[Servo, list[Servo]]):
        if isinstance(servo_list, list):
            for servo in servo_list:
                self._add_servo(servo)
        else:
            self._add_servo(servo_list)

    def _remove_servo(self, servo):
        if servo.servo_id in self.servos:
            del self.servos[servo.servo_id]
            self.total_servos -= 1
        else:
            raise ValueError(f"Unable to find servo with id {servo.servo_id}")

    def remove_servos(self, servo_list: Union[Servo, list[Servo]]):
        if isinstance(servo_list, list):
            for servo in servo_list:
                self._remove_servo(servo)
        else:
            self._remove_servo(servo_list)

    def remove_all_servos(self):
        self.servos.clear()

    def get_total_servos(self):
        return self.total_servos

    def print_group_info(self):
        pass

    def sync_get_positions(self, is_radian: bool = False):
        ref_servo = self.servos[
            list(self.servos)[0]
        ]  # Taking the first servo's config as reference
        port_h = ref_servo.port_handler
        packet_h = ref_servo.packet_handler
        start_addr = ref_servo.control_table.ADDR_PRESENT_POSITION
        data_length = 4

        sync_read = GroupSyncRead(port_h, packet_h, start_addr, data_length)

        for dxl_id in self.servos.keys():
            sync_read.addParam(dxl_id=dxl_id)

        comm_result = sync_read.txRxPacket()
        self._print_error(comm_result=comm_result, packet_h=packet_h)

        current_positions = []
        for dxl_id in self.servos.keys():
            if sync_read.isAvailable(dxl_id, start_addr, data_length):
                raw_position = sync_read.getData(dxl_id, start_addr, data_length)

                if is_radian:
                    angle = (
                        pi * float(raw_position) / self.servos[dxl_id].middle_pos_val
                    )
                else:
                    angle = (
                        180 * float(raw_position) / self.servos[dxl_id].middle_pos_val
                    )
                current_positions.append(angle)
            else:
                raise RuntimeError(
                    f"group_sync_read failed for servo with id: {dxl_id}"
                )

        sync_read.clearParam()

        return current_positions

    def sync_set_positions(self, goal_positions: list[float], is_radian: bool = False):
        ref_servo = self.servos[list(self.servos)[0]]
        port_h = ref_servo.port_handler
        packet_h = ref_servo.packet_handler
        start_addr = ref_servo.control_table.ADDR_GOAL_POSITION
        data_length = 4

        sync_write = GroupSyncWrite(
            port=port_h, ph=packet_h, start_address=start_addr, data_length=data_length
        )

        for i, dxl_id in enumerate(self.servos.keys()):

            if is_radian:
                goal_pos = int(
                    self.servos[dxl_id].middle_pos_val * goal_positions[i] / pi
                )
            else:
                goal_pos = int(
                    self.servos[dxl_id].middle_pos_val * goal_positions[i] / 180
                )

            param_data = utils.convert_to_bytes(value=goal_pos, data_bytes=data_length)
            success = sync_write.addParam(dxl_id=dxl_id, data=param_data)

            if not success:
                raise RuntimeError(f"Failed to set goal_pos for servo with id {dxl_id}")

            comm_result = sync_write.txPacket()
            self._print_error(comm_result=comm_result, packet_h=packet_h)

            sync_write.clearParam()

    def sync_torques_enabled(self, is_enabled: bool = False):
        ref_servo = self.servos[list(self.servos)[0]]
        port_h = ref_servo.port_handler
        packet_h = ref_servo.packet_handler
        start_addr = ref_servo.control_table.ADDR_TORQUE_ENABLE
        data_length = 1

        sync_write = GroupSyncWrite(
            port=port_h, ph=packet_h, start_address=start_addr, data_length=data_length
        )

        for dxl_id in self.servos.keys():
            param_data = [1 if is_enabled else 0]
            success = sync_write.addParam(dxl_id=dxl_id, data=bytes(param_data))
            if not success:
                raise RuntimeError(f"Failed to set torque for servo with ID {dxl_id}")

        comm_result = sync_write.txPacket()
        self._print_error(comm_result=comm_result, packet_h=packet_h)

        sync_write.clearParam()

    def bulk_read(self):
        pass

    def bulk_write(self):
        pass

    def _print_error(self, comm_result, packet_h) -> None:
        if comm_result != COMM_SUCCESS:
            raise RuntimeError(f"\n{packet_h.getTxRxResult(comm_result)}")

    # def convert_to_bytes(self, value, data_bytes):
    #     # Referenced from - https://github.com/huggingface/lerobot/blob/main/lerobot/common/robot_devices/motors/dynamixel.py
    #
    #     if data_bytes == 1:
    #         data = [
    #             DXL_LOBYTE(DXL_LOWORD(value)),
    #         ]
    #     elif data_bytes == 2:
    #         data = [
    #             DXL_LOBYTE(DXL_LOWORD(value)),
    #             DXL_HIBYTE(DXL_LOWORD(value)),
    #         ]
    #     elif data_bytes == 4:
    #         data = [
    #             DXL_LOBYTE(DXL_LOWORD(value)),
    #             DXL_HIBYTE(DXL_LOWORD(value)),
    #             DXL_LOBYTE(DXL_HIWORD(value)),
    #             DXL_HIBYTE(DXL_HIWORD(value)),
    #         ]
    #     else:
    #         raise NotImplementedError(
    #             f"Value of the number of bytes to be sent is expected to be in [1, 2, 4], but "
    #             f"{data_bytes} is provided instead."
    #         )
    #     return data

    # def get_servo_ids(self):
    #
    #     if self.protocol_version == 1:
    #         print("The method get_servo_ids only works with Protocol 2.0")
    #         quit()
    #
    #     found_servos = []
    #     dxl_data, dxl_comm_result = self.packet_handler.broadcastPing(port=self.port_handler)
    #     if dxl_comm_result != COMM_SUCCESS:
    #         print(f"{self.packet_handler.getTxRxResult(dxl_comm_result)}")
    #
    #     for ids in dxl_data:
    #         found_servos.append(ids)
    #     return found_servos
