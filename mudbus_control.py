from pymodbus.client import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

class GripperControl:
    def __init__(self, port: str, baudrate: int = 115200):
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

    def _send_modbus_command(self, address: int, register_address: int, value: int) -> bool:
        """Send a Modbus RTU command to the device.
        :return: True if the command was successful, False otherwise.
        """
        flag = False  # Initialize flag as False
        try:
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
        except Exception as e:
            print(f"An error occurred: {e}")
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

    def gripper_reset(self, open_position: int = 100):
        """Open the grippers to a specified position."""
        if not 100 <= open_position <= 560:
            print("Invalid position value. Position should be between 100 and 560.")
            return
        open_left_flag = self._send_modbus_command(self.left_address, self.pos_register_address, open_position)
        open_right_flag = self._send_modbus_command(self.right_address, self.pos_register_address, open_position)
        if open_left_flag and open_right_flag:
            print(f"Write reset successful! Response Data: {open_position}")

    def gripper_close(self, close_position: float):
        """Close the grippers to a specified position."""
        if not 100 <= close_position <= 560:
            print("Invalid position value. Position should be between 100 and 560.")
            return
        write_left_flag = self._send_modbus_command(self.left_address, self.pos_register_address, int(close_position))
        write_right_flag = self._send_modbus_command(self.right_address, self.pos_register_address, int(close_position))
        if write_left_flag and write_right_flag:
            print(f"Write close successful! Response Data: {close_position}")