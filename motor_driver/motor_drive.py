# Write code to send commands to arduino .ino file
# Use serial communication to send commands to arduino
# Use pyserial library to send commands to arduino
# https://bobbyhadz.com/blog/python-attributeerror-module-serial-has-no-attribute-serial
# https://www.instructables.com/Python-pySerial-Arduino-DC-Motor/
# https://learn.adafruit.com/adafruit-motor-shield-v2-for-arduino/using-dc-motors

import serial
import time
import keyboard

# Create serial object
board = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Wait for serial to connect
time.sleep(3)

# take inputs from computer's arrow keys and send commands: forward, backward, left, right, or hold to arduino
# use while loop to keep taking inputs from user
while True:
    # Get input from user
    event = keyboard.read_event()
    # if the a key is pressed down send command to arduino
    if event.event_type == 'down' and event.name == 'a':
        print("LEFT")
        board.write('a'.encode())
    if event.event_type == 'down' and event.name == 'w':
        print("UP")
        board.write('w'.encode())
    if event.event_type == 'down' and event.name == 's':
        print("DOWN")
        board.write('s'.encode())
    if event.event_type == 'down' and event.name == 'd':
        print("RIGHT")
        board.write('d'.encode())
    # while no key is pressed, send hold command to arduino stop motor drift
    if event.event_type == 'up' and event.name=='a':
        print("HOLD")
        board.write('d'.encode())
        board.write('h'.encode())
    if event.event_type == 'up' and event.name=='w':
        print("HOLD")
        board.write('s'.encode())
        board.write('h'.encode())
    if event.event_type == 'up' and event.name=='s':
        print("HOLD")
        board.write('w'.encode())
        board.write('h'.encode())
    if event.event_type == 'up' and event.name=='d':
        print("HOLD")
        board.write('a'.encode())
        board.write('h'.encode())
    # Send command to arduino
    # board.write(key.encode())
    # Read arduino's response
    # arduino_response = board.readline()
    # Print arduino's response
    # print(arduino_response.decode('utf-8'))
