from e_gripper_mudbus_control import GripperControl

if __name__ == "__main__":
    # Serial port settings
    
    port = "COM9"  # Change to your COM port
    gripper = GripperControl(port)

    raw_position = gripper.map_position(100)
    print(f"Raw position full open: {raw_position}")

    raw_position = gripper.map_position(0)
    print(f"Raw position full close: {raw_position}")

    raw_position = gripper.map_position(50)
    print(f"Raw position 50% : {raw_position}")