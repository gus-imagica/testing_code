# -*- coding: utf-8 -*-
"""
Created on Tue May  2 14:05:22 2017

This class contains useful functions for connecting to and controlling the
Tunable Light Source from Newport.

@author: Gus
"""

import serial

class TLS(object):
    
    def __init__(self, port = "COM5", timeout_s = 5):
        # Find resources
        self.ser = serial.Serial(port, timeout = timeout_s, baudrate = 9600, bytesize=8, parity = 'N', stopbits = 1)
        
        self.info = self.query("INFO?")
        
    
    # Sends a command, returns 1 if successful 0 otherwise
    def command(self, string):
        cmd = string+'\r\n'
        self.ser.write(cmd.encode("utf-8"))
        echo = self.ser.readline()
        if len(echo)>0:
            echo = echo.decode('ascii')
        # print('Receiving...'+out.decode('ascii'))
        if string in echo: # responses always start with the command
            return 1
        else:
            return 0        
    
    # Sends a query and returns the response without the original command
    def query(self, string):
        cmd = string+'\r\n'
        self.ser.write(cmd.encode("utf-8"))
        echo = self.ser.readline()
        out = self.ser.readline()
        if len(out)>0:
            out = out.decode('ascii')
        else:
            print("No response")
            out = None
        return out
    
    # set the output wavelength to lam. Will cut off at 100
    def set_lambda(self, lam):
        lam = max(100, min(1000,lam))
        
        if isinstance(lam, int):
            numstr = str(lam)
        
        else:
            numstr = '{0:0.3f}'.format(lam)
        
        return self.command("GOWAVE "+numstr)
    
    # gets the value of lambda
    def get_lambda(self):
        ret = self.query("WAVE?")
        if ret is not None:
            try:
                return float(ret)
            except Exception:
                print("response to WAVE? "+ret)
                return -1
        else:
            return None
    
    # set the wavelength
    def step_lambda(self, steps=1):
        steps = int(steps)
        return self.command("STEP "+steps)
    
    # True closes the shutter and False opens it.
    def shutter(self, engaged):
        if engaged:
            return self.command("SHUTTER O") # Counterintuitively, this blocks the light
        if not engaged:
            return self.command("SHUTTER C") # This allows light through the slit
    
    # moves the filter wheel
    def filterW(self, setting):
        if isinstance(setting,int):
            if setting < 7:
                if setting > 0:
                    return self.command("FILTER "+str(setting))
        else: return 0
                    
    
    def close(self):
        self.ser.close()
    
    
        