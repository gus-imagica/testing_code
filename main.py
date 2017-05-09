# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:05:43 2017

@author: Gus
"""

import keysight
import newportTLS
import pyvisa
import time

def analyse_dark_current(inst, start_voltage, stop_voltage, steps):
    sensor_string = ":sens:func \"CURR\"; :sens:curr:rang:auto off; :sens:curr:rang 2.E-7;"
    sensor_string += ":sens:curr:aper:auto on; :sens:curr:aper:auto:mode med"
    source_string = ":sour:func:mode volt; :sour:volt:mode swe; :sour:volt:star "+str(start_voltage)+";"
    source_string += ":sour:volt:stop "+str(stop_voltage)+"; :sour:volt:poin "+str(steps)
    trigger_string = ":trig:sour aint; :trig:coun "+str(steps)+"; :trig:acq:del 1; :trig:tim 1.2"
    
    inst.inst.write(sensor_string)
    inst.inst.write(source_string)
    inst.inst.write(trigger_string)
    inst.inst.write(":outp:stat on; :inp on")
    
    inst.inst.write(":init (@1)")
    
    inst.inst.write(":syst:time:tim:coun:res:auto on")
    inst.inst.write(":init:acq")
    inst.inst.write(":form:elem:sens CURR,TIME")
    
    for step in range(steps):
        print(inst.inst.query(":sens:data? curr, 1"))

try:
#    inst = newportTLS.TLS()
    
    inst = keysight.keysight()
    
    inst.enable_output_voltage()
    
#    inst.set_output_voltage(4)
    
    inst.enable_sensing()
    
    analyse_dark_current(inst,0,5,15)
    
    inst.get_current()
    inst.get_temperature()
except pyvisa.errors.VisaIOError as e:
    print("Timed out waiting for a response. Make sure all sensors are connected.")
    print(e)

