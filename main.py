from e_gripper_mudbus_control import GripperControl

if __name__ == "__main__":
    # Serial port settings
    
    port = "COM9"  # Change to your COM port
    gripper = GripperControl(port)
    reset_position = 100 #default
    close_position = 200
    speed = 100
    
    # Example usage
    gripper.set_speed(speed)
    gripper.gripper_close(close_position)  # Close grippers to position range is [100, 555], max=560
    #gripper.gripper_reset(reset_position)  # Open grippers to default position (100)
    #gripper.read_position()  # Read current positions
    # gripper.read_PID(key="P")   #20
    # gripper.read_PID(key="I")   #0
    # gripper.read_PID(key="D")   #0
    # gripper.set_PID(key="P", value=50)
    # gripper.set_PID(key="D", value=0)
    # gripper.set_PID(key="I", value=5)
