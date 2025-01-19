from e_gripper_mudbus_control_one_init import GripperControl
import time
if __name__ == "__main__":
    
    gripper = GripperControl(port="/dev/ttyUSB0", baudrate=115200)
    result = gripper._read_modbus_register(id_address=2, register_address=2, num_registers=1)
    time.sleep(0.1)
    # result = gripper._send_modbus_command(2, 2, 200)
    if result is not None:
        print(f"Read registers: {result}")
    else:
        print("Failed to read registers.")