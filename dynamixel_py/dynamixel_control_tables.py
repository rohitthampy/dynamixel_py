class XL330:
    # Control table addresses for XL330-M288-T

    # EEPROM Area - Permanently stored in memory once changed
    ADDR_MODEL_NUMBER = 0
    ADDR_MODEL_INFORMATION = 2
    ADDR_FIRMWARE_VERSION = 6
    ADDR_HOMING_OFFSET = 20

    # RAM Area
    ADDR_TORQUE_ENABLE = 64
    ADDR_GOAL_POSITION = 116
    ADDR_PRESENT_POSITION = 132


class XC330:
    # Control table addresses for XC330
    # EEPROM Area - Permanently stored in memory once changed
    ADDR_MODEL_NUMBER = 0
    ADDR_MODEL_INFORMATION = 2
    ADDR_FIRMWARE_VERSION = 6
    ADDR_HOMING_OFFSET = 20

    # RAM Area
    ADDR_TORQUE_ENABLE = 64
    ADDR_GOAL_POSITION = 116
    ADDR_PRESENT_POSITION = 132


class XL430:
    # Control table addresses for XL430
    # EEPROM Area - Permanently stored in memory once changed
    ADDR_MODEL_NUMBER = 0
    ADDR_MODEL_INFORMATION = 2
    ADDR_FIRMWARE_VERSION = 6
    ADDR_HOMING_OFFSET = 20

    # RAM Area
    ADDR_TORQUE_ENABLE = 64
    ADDR_GOAL_POSITION = 116
    ADDR_PRESENT_POSITION = 132


class AX12:
    # Control table addresses for AX12
    # EEPROM Area - Permanently stored in memory once changed
    ADDR_MODEL_NUMBER = 0
    ADDR_FIRMWARE_VERSION = 2

    # RAM area
    ADDR_TORQUE_ENABLE = 24
    ADDR_GOAL_POSITION = 30
    ADDR_PRESENT_POSITION = 36


class MX12:
    # Control table addresses for MX12
    # EEPROM Area - Permanently stored in memory once changed
    ADDR_MODEL_NUMBER = 0
    ADDR_FIRMWARE_VERSION = 2

    # RAM area
    ADDR_TORQUE_ENABLE = 24
    ADDR_GOAL_POSITION = 30
    ADDR_PRESENT_POSITION = 36


control_tables = {
    1: {"AX12": AX12, "MX12": MX12},
    2: {"XL330": XL330, "XC330": XC330, "XL430": XL430},
}

if __name__ == "__main__":
    for items in control_tables:
        print(items)
