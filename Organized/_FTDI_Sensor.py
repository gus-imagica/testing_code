# -*- coding: utf-8 -*-
"""
Created on Thu May 11 15:38:22 2017

This class controls the Sony sensors through the FTDI chip.

@author: Gus
"""

import serial
import numpy as np
import time
import matplotlib.pyplot as plt

""" settings """
divider = ","

class sensor(object):
    
    def __init__ (self, port = "COM4", timeout_s = 10, print_out = False):
        self.print_out = print_out
        self.timeout_s = timeout_s
        self.ser = serial.Serial(port, timeout = self.timeout_s, baudrate = 115200)
        if not self.ser.isOpen():
            raise Exception("Serial port at "+port+" was not opened successfully.")
        self.ser.flush()
        time.sleep(0.1)
        self.command("F,")
        self.command("E1")
        self.integ_ms = None
        self.reps = None
        
    def query(self, string, expected = ""):
        cmd = string+'\r'
        cmd_bin = cmd.encode("utf-8")
        self.ser.write(cmd_bin)
        if self.print_out:
            print(cmd_bin)
        time.sleep(0.001)
        out = b""
        # Look for buffered data
#        trys = 200
#        while trys > 0:
        start_t = time.time()
        while True:
            data_count = self.ser.inWaiting()
#            if self.print_out:
#                print("data_count: ", data_count)
            if data_count>0:
                out1 = self.ser.read(data_count)
                out += out1
                #check for the return character
                out1 = out1.decode('ascii')
                if "\r" in out1:
                    break
                else:
                    continue
            if time.time()-start_t > self.timeout_s:
                out = None
                break
            
        if out is not None:
            out = out.decode('ascii')
            out = out.strip()
            if self.print_out:
                print(repr(out))
                print(len(out))
                print(self.ser.inWaiting())
        else:
            if self.print_out:
                print("No response")
            out = None
        return out
    
    def command(self, string, expected = ""):
        cmd = string+'\r'
        self.ser.write(cmd.encode("utf-8"))
        if self.print_out:
            print("Sent: ", repr(cmd))
        # Look for buffered data
        outp = ""
        start_t = time.time()
        while True:
            time.sleep(0.001)
            data_count = self.ser.inWaiting()
            if self.print_out:
                print("data_count: ", data_count)
            if data_count>0:
                out = self.ser.read(data_count)
                out = out.decode('ascii')
#                if self.print_out:
#                    print(repr(out))
                outp += out
                if "\r" in outp:
                    break
                else:
                    continue
            if time.time()-start_t > self.timeout_s:
                out = None
                break
        if self.print_out:
            print("Received: ", repr(outp))
            
        if expected in outp:
            return True
        else:
            return False
    
    def get_spect(self):
        self.command("S", expected = "DONE")
        ret = self.query("G")
        ret = ret.strip(divider)
        arr = ret.split(divider)
#        if self.print_out:
#            print(repr(arr))
        intarr = map(int, arr)
        return np.array(list(intarr))
    
    def set_aper(self, time_ms):
        time_ms = int(time_ms)
        self.command("I%s" % time_ms, expected = "I")
        self.integ_ms = time_ms
        
    def set_reps(self, reps):
        self.command("R%s" % reps)
        self.reps = reps
        
    def set_trigger(self):
        self.command("E3")
    
    def close(self):
        self.ser.close()
        
    def print_frame(self):
        frame = self.get_spect()
        plt.figure(figsize = (12, 7))
        plt.plot(frame, ".", linewidth = 0.5, ms = 1.5)