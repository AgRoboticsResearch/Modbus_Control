from e_gripper_mudbus_control_one_init import GripperControl
import time


if __name__ == "__main__":


    gripper = GripperControl(port="/dev/ttyUSB_girpper", baudrate=115200)

    # Read all info
    gripper.read_all_info_oneside(gripper.LEFT_ADDRESS)
    gripper.read_all_info_oneside(gripper.RIGHT_ADDRESS)