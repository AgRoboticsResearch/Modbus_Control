from e_gripper_mudbus_control_one_init import GripperControl
import time

if __name__ == "__main__":
    # Serial port settings
    
    port = "/dev/ttyUSB_girpper"  # Change to your COM port
    gripper = GripperControl(port)
    reset_position = 100 #default
    close_position = 200
    speed = 1022
    position = [100, 20, 100, 10]
    # Example usage
    for _ in range(4):
        for i in position:
            gripper.set_position_percent(i)
            time.sleep(0.5) 

    # gripper.set_position_percent(80)
    # # gripper.set_position_percent(70)  # Close grippers to position range is [100, 555], max=560
    # # # gripper.gripper_reset(reset_position)  # Open grippers to default position (100)
    # # #gripper.read_position()  # Read current positions
    # gripper.read_PID(key="P")   #20
    # # gripper.set_position_percent(10)
    # # # gripper.read_PID(key="P")   #20
    # gripper.set_position_percent(20)
    # gripper.read_PID(key="I")   #0
    # gripper.read_PID(key="D")   #0
    # gripper.set_PID(key="P", value=50)
    # gripper.set_PID(key="D", value=0)
    # gripper.set_PID(key="I", value=5)
    # gripper.close()
