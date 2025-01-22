from e_gripper_mudbus_control_one_init import GripperControl
import time
if __name__ == "__main__":
    
    gripper = GripperControl(port="/dev/ttyUSB_girpper", baudrate=115200)
    result = gripper._read_modbus_register(id_address=2, register_address=2, num_registers=1)
    while True:
        time.sleep(0.001)
        left_position, right_position = gripper.read_position()
        print(f"Left Position: {left_position}")
        print(f"Right Position: {right_position}")
