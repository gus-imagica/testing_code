# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:05:43 2017

@author: Gus
"""

import keysight
import newportTLS
import pyvisa
import time

try:
    inst = newportTLS.TLS()
    
    inst = keysight.keysight()
    
    inst.enable_output_voltage()
    
    inst.set_output_voltage(4)
    
    inst.enable_sensing()
    
    inst.get_current()
    
    temper = inst.get_temperature()
    
    print("Temperature " + str(temper))
    
except pyvisa.errors.VisaIOError as e:
    print("Timed out waiting for a response. Make sure all sensors are connected.")
    print(e)

