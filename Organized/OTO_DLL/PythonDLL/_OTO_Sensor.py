# -*- coding: utf-8 -*-
"""
Created on Thu May 11 15:38:22 2017

This class controls the Sony sensors through the FTDI chip.

@author: Gus
"""

from ctypes import *
#OTO USB2.0 spectrameter's VID & PID
VID = 1592
PID = 2732

# This needs to be the 64bit version copied from the SDK, not the default 32bit DLL.
dll_path = r"UserApplication"
OTOdll = windll.LoadLibrary(dll_path)

def open_device(index = 0):
    intDeviceHandle = c_int()
    OTOdll.UAI_SpectrometerOpen(index, byref(intDeviceHandle),VID,PID)
    return(intDeviceHandle)

def close_device(deviceHandle):
    OTOdll.UAI_SpectrometerClose(deviceHandle)

def count_devices():
    #Check how many device is connected with PC.
    intDeviceCount = c_int(0)
    OTOdll.UAI_SpectrometerGetDeviceAmount(VID,PID,byref(intDeviceCount))
    return(intDeviceCount.value)
    
# This function kills the kernel. No idea why.
def get_device_list():
    intNumber = c_int(0)
    OTOdll.UAI_SpectrometerGetDeviceList(byref(intNumber),None)
    #intList = create_string_buffer(sizeof(c_int*intNumber.value*2))
    intList = create_string_buffer(b"0000000000000000", sizeof(c_int*intNumber.value*2))
    OTOdll.UAI_SpectrometerGetDeviceList(byref(intNumber),intList)
    return(intNumber.value, intList.value)

def get_model(deviceHandle):
    modelName = create_string_buffer(500)
    OTOdll.UAI_SpectrometerGetModelName(deviceHandle,byref(modelName))
    return(repr(modelName.value))

#
#import serial
#import numpy as np
#from time import sleep
#import matplotlib.pyplot as plt
#
#class sensor(object):
#    
#    def __init__ (self, port = "COM4", timeout_s = 1, print_out = False):
#        self.print_out = print_out
#        self.ser = serial.Serial(port, timeout = timeout_s, baudrate = 115200)
#        if not self.ser.isOpen():
#            raise Exception("Serial port at "+port+" was not opened successfully.")
#        self.ser.flush()
#        sleep(0.1)
#        self.command("F ")
#        self.command("E1")
#        self.integ_ms = None
#        self.reps = None
#        
#    def query(self, string, expected = ""):
#        cmd = string+'\r'
#        cmd_bin = cmd.encode("utf-8")
#        self.ser.write(cmd_bin)
##        if self.print_out:
##            print(cmd_bin)
#        sleep(0.001)
#        out = b""
#        # Look for buffered data
##        trys = 200
##        while trys > 0:
#        while True:
#            data_count = self.ser.inWaiting()
#            if data_count>0:
#                out1 = self.ser.read(data_count)
#                out += out1
#                #check for the return character
#                out1 = out1.decode('ascii')
#                if "\r" in out1:
#                    break
#                else:
#                    continue
#            
#        out = out.decode('ascii')
#        out = out.strip()
#            
#            
#        if out is not None:
#            if self.print_out:
#                print(repr(out))
#                print(len(out))
#                print(self.ser.inWaiting())
#        else:
#            if self.print_out:
#                print("No response")
#            out = None
#        return out
#    
#    def command(self, string, expected = ""):
#        cmd = string+'\r'
#        self.ser.write(cmd.encode("utf-8"))
#        
#        # Look for buffered data
#        outp = ""
#        while True:
#            sleep(0.001)
#            data_count = self.ser.inWaiting()
#            if data_count>0:
#                out = self.ser.read(data_count)
#                out = out.decode('ascii')
#                outp += out
#                if "\r" in outp:
#                    break
#                else:
#                    continue
#        
#        if self.print_out:
#            print(repr(outp))
#            
#        if expected in outp:
#            return True
#        else:
#            return False
#    
#    def get_spect(self):
#        self.command("S", expected = "DONE")
#        ret = self.query("G")
#        return np.array(list(map(int,ret.split())))
#    
#    def set_aper(self, time_ms):
#        self.command("I%s" % time_ms, expected = "I")
#        self.integ_ms = time_ms
#        
#    def set_reps(self, reps):
#        self.command("R%s" % reps)
#        self.reps = reps
#        
#    def set_trigger(self):
#        self.command("E3")
#    
#    def close(self):
#        self.ser.close()
#        
#    def print_frame(self):
#        frame = self.get_spect()
#        plt.figure(figsize = (12, 7))
#        plt.plot(frame, ".", linewidth = 0.5, ms = 1.5)