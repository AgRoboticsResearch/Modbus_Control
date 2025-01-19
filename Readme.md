# Gripper Control Module
This module provides a Python interface to control a gripper device using Modbus RTU communication. It supports the following functions:

1. Reset: Open the gripper to the default position.

2. Close: Close the gripper to a specified position.

3. Read Position: Read the current position of the gripper.

## Installation
```
pip install pymodbus
pip install pyserial
```

## Uesage
### The setting of timeout
The timeout should be as small as possible to speed up the response, but tests have found that when the timeout < 0.005 causes the read to fail. In this code it is set to 0.005.

### In Ubuntu
```
dmesg | grep tty
sudo chmod 666 /dev/ttyUSB0   #if the port is USB0
```
The usage is all in main.py.
#### 1.Import the Module:
Import the GripperControl class from the module:
```
from gripper_control import GripperControl
```
#### 2.Initialize the Gripper:
Create an instance of the GripperControl class by specifying the serial port:
```
port = "COM9"  # Replace with your COM port
gripper = GripperControl(port)
```
## Functions
#### 1. Reset the Gripper
Open the gripper to the default position 100. You can modify the location of the initialization in according to your needs.
```
gripper.gripper_reset(open_position) 
```

#### 2. Close the Gripper
Close the gripper to grasp. You can set the position in according to your needs. However, please note that the maximum position should not exceed 560.
```
gripper.gripper_close(close_position)  
```
#### 3. Read the Gripper Position
Read the current position of the gripper.
```
gripper.read_position(read_num_registers: int = 1) 
```
#### 4. Value in each register
```
00003 最高速度 1000 #200-1023
00004 循环模式 0
00006 目标回写 1
00007 极性    0
00008 目标锁定 1
00009 PID_P  50
00010 PID_I  5
00010 PID_D  0
00014 死区   15
00015 最大扭矩 800
```

