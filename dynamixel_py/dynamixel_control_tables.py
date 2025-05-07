class XL330:
    # Control table addresses for XL330-M288-T

    # EEPROM Area - Permanently stored in memory once changed
    ADDR_MODEL_NUMBER = 0
    ADDR_MODEL_INFORMATION = 2
    ADDR_FIRMWARE_VERSION = 6
    ADDR_PRESENT_POSITION = 132
    ADDR_HOMING_OFFSET = 20

    # RAM Area
    ADDR_TORQUE_ENABLE = 64
    ADDR_GOAL_POSITION = 116

class XC330:
    # Control table addresses for XC330
    # EEPROM Area - Permanently stored in memory once changed
    ADDR_MODEL_NUMBER = 0
    ADDR_MODEL_INFORMATION = 2
    ADDR_FIRMWARE_VERSION = 6
    ADDR_PRESENT_POSITION = 132
    ADDR_HOMING_OFFSET = 20

    # RAM Area
    ADDR_TORQUE_ENABLE = 64
    ADDR_GOAL_POSITION = 116
    pass

class AX12:
    pass

class MX12:
    pass


# control_tables = [{"AX12": AX12, "MX12": MX12}, # Protocol 1.0 motors
#                   {"XL330": XL330, "XC330": XC330}] # Protocol 2.0 motors

control_tables = {1:{"AX12": AX12, "MX12": MX12},
                  2: {"XL330": XL330, "XC330": XC330}}

if __name__ == "__main__":
    for items in control_tables:
        print(items)