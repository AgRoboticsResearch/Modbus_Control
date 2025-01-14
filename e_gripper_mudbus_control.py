from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

class GripperControl:
    def __init__(self, port: str, baudrate: int = 115200, raw_max_position: int = 100, raw_min_position: int = 580):
        """
        Initialize the GripperControl class.
        :param port: Serial port (e.g., 'COM9').
        :param baudrate: Baud rate (default is 115200).
        """
        self.port = port
        self.baudrate = baudrate
        self.left_address = 1  # Device address for left gripper
        self.right_address = 0  # Device address for right gripper
        self.pos_register_address = 2  # Position register address
        self.speed_register_address = 3
        self.RAW_MAX_POSITION = raw_max_position # full open
        self.RAW_MIN_POSITION = raw_min_position # full close
        print(f"GripperControl initialized using port and baudrate: {port}, {baudrate}")

    def _send_modbus_command(self, address: int, register_address: int, value: int) -> bool:
        """Send a Modbus RTU command to the device.
        :return: True if the command was successful, False otherwise.
        """
        flag = False  # Initialize flag as False
        
        client = ModbusSerialClient(port=self.port, baudrate=self.baudrate, timeout=1)
        if client.connect():
            try:
                response = client.write_register(register_address, value, slave=address)
                if response.isError():
                    print(f"Error: {response.message}")
                else:
                    flag = True
                    
            except Exception as e:
                print(f"An error occurred while sending command: {e}")
            finally:
                client.close()
        else:
            print("Failed to connect to the Modbus device.")
        
        return flag

    def _read_modbus_register(self, address: int, register_address: int, num_registers: int):
        """Read a Modbus register value from the device."""
        client = ModbusSerialClient(port=self.port, baudrate=self.baudrate, timeout=5)
        if client.connect():
            try:
                response = client.read_holding_registers(register_address, num_registers, slave=address)
                if response.isError():
                    print(f"Read Error: {response}")
                    return []
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.BIG)
                    return [decoder.decode_16bit_uint() for _ in range(num_registers)]
            finally:
                client.close()
        else:
            print("Failed to connect to the Modbus device.")
            return []

    def read_position(self, read_num_registers: int = 1):
        """Read the current position of both left and right grippers."""
        left_position = self._read_modbus_register(self.left_address, self.pos_register_address, read_num_registers)
        right_position = self._read_modbus_register(self.right_address, self.pos_register_address, read_num_registers)
        print(f"Position in left gripper: {left_position}")
        print(f"Position in right gripper: {right_position}")

    def set_speed(self, speed: int):
        """
        Set the maximum speed for both left and right grippers.
        :param speed: Target speed value (range 200-1023).
        """
        # Check speed range
        if speed < 200 or speed > 1023:
            print("Error: Speed value must be between 200 and 1023.")
            return

        left_speed = self._send_modbus_command(self.left_address, self.speed_register_address, speed)
        right_speed = self._send_modbus_command(self.right_address, self.speed_register_address, speed)
        if left_speed and right_speed:
                print(f"Right gripper speed setting successful: {speed}")
    
    def map_position(self, percent_position: float):
        """Map the percent position to raw position. 0% to self.RAW_MIN_POSITION, 100% to self.RAW_MAX_POSITION."""
        return int(self.RAW_MIN_POSITION + (self.RAW_MAX_POSITION - self.RAW_MIN_POSITION) * percent_position / 100)

        
    def set_position_raw(self, close_position: float):
        """Close the grippers to a specified position."""
        if not self.RAW_MAX_POSITION <= close_position <= self.RAW_MIN_POSITION:
            print("Invalid position value. Position should be between 100 and 560.")
            return
        write_left_flag = self._send_modbus_command(self.left_address, self.pos_register_address, int(close_position))
        write_right_flag = self._send_modbus_command(self.right_address, self.pos_register_address, int(close_position))
        if write_left_flag and write_right_flag:
            print(f"Write close successful! Response Data: {close_position}")
