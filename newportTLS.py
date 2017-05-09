# -*- coding: utf-8 -*-
"""
Created on Tue May  2 14:05:22 2017

@author: Gus
"""

import serial

class TLS(object):
    
    def __init__(self, port = "COM5", timeout_s = 1):
        # Find resources
        self.ser = serial.Serial(port, timeout = timeout_s, baudrate = 9600, bytesize=8, parity = 'N', stopbits = 1)
        
        self.info = self.query("INFO?")
        
    
    # Sends a command, returns 1 if successful 0 otherwise
    def command(self, string):
        cmd = string+'\r\n'
        self.ser.write(cmd.encode("utf-8"))
        out = self.ser.read(100)
        if len(out)>0:
            response = out.decode('ascii')
        # print('Receiving...'+out.decode('ascii'))
        if string in response: # responses always start with the command
            return 1
        else:
            return 0        
    
    # Sends a query and returns the response without the original command
    def query(self, string):
        cmd = string+'\r\n'
        self.ser.write(cmd.encode("utf-8"))
        out = self.ser.read(100)
        if len(out)>0:
            response = out.decode('ascii')
        # print('Receiving...'+out.decode('ascii'))
        resp = response.replace(cmd, "", 1) # responses always start with the command
        return resp
    
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
            return float(ret)
        else:
            return None
    
    # set the wavelength
    def step_lambda(self, steps=1):
        steps = int(steps)
        return self.command("STEP "+steps)
    
    def close(self):
        self.ser.close()
    
    
        