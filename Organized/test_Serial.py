# -*- coding: utf-8 -*-
"""
Created on Mon May  8 13:07:26 2017

This function connects to a serial port and allows commands to be sent.

@author: Gus
"""

import serial

ser = serial.Serial("COM4", timeout = 3, baudrate = 115200)

print(ser.isOpen())

print(ser.name)

while True:
    cmd = input("Enter command or 'exit':")
    if cmd == 'exit':
        ser.close()
        break
    else:
        cmd = cmd+'\r'
        ser.write(cmd.encode("utf-8"))
        echo = ser.readline()
        print('Received: '+repr(echo.decode('ascii')))
#        out = ser.readline()
#        print('Received: '+out.decode('ascii'))