# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:05:43 2017

@author: Gus
"""

import keysight
import pyvisa

try:
    inst = keysight.keysight()
    
    inst.inst.write(":sour:func:mode volt")
    inst.inst.write(":sour:volt:mode swe")
    inst.inst.write(":sour:volt:star 0.0")
    inst.inst.write(":sour:volt:stop 10.0")
    
    inst.inst.write(":sour:volt:poin 21")
    inst.inst.write(":sour:swe:sta sing")
    
    inst.set_output_voltage(4)
    
    inst.enable_sensing()
    inst.get_current()
    inst.get_temperature()
except pyvisa.errors.VisaIOError as e:
    print("Timed out waiting for a response. Make sure all sensors are connected.")

