# -*- coding: utf-8 -*-
"""
Created on Mon May  8 13:07:26 2017

@author: Gus
"""

import serial

ser = serial.Serial("COM5", timeout = 3)

print(ser.isOpen())

print(ser.name)

while True:
    cmd = input("Enter command or 'exit':")
        # for Python 2
    # cmd = input("Enter command or 'exit':")
        # for Python 3
    if cmd == 'exit':
        ser.close()
        break
    else:
        cmd = cmd+'\r\n'
        ser.write(cmd.encode("utf-8"))
        echo = ser.readline()
        out = ser.readline()
        print('Receiving... '+out.decode('ascii'))