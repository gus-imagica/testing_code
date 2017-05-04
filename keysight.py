# -*- coding: utf-8 -*-
"""
Created on Tue May  2 14:05:22 2017

@author: Gus
"""

import visa

class keysight(object):
    
    def __init__(self, self_cal = False, self_test = False, timeout_ms = 10000, default_connection = 0):
        # Find resources
        rm = visa.ResourceManager()
        rl = rm.list_resources()
        # Get the keysight
        if len(rl)>1:
            print("Available resources: ",rl)
            print("Connecting to "+rl[default_connection])
        inst = rm.open_resource(rl[default_connection])
        self.inst = inst
        self.set_timeout(timeout_ms)

        if self_cal:
            self.self_calibrate()
        if self_test:
            self.self_test()
            
        self.reset()
        
    
    # Resets to default settings
    def reset(self):
        return(self.inst.write("*RST"))
    
    def device_info(self):
        return(self.inst.query("*IDN?"))
    
    # Runs the self test
    # Returns True for a pass, False for a failure.
    # All test leads shoud be removed when the self-test is run.
    def self_test(self):
        result = self.inst.query("*TST?")
        if "0" in result:
            print("self-test PASS")
            return(True)
        else:
            print("self-test FAIL")
            return(False)
        
    def self_calibrate(self):
        timo = self.timeout
        self.set_timeout(240000) # calibration takes a long time. (4min)
        result = self.inst.query("*CAL?")
        self.set_timeout(timo)
        print(result)
        if "0" in result:
            print("self-calibrate PASS")
            return(True)
        else:
            print("self-calibrate FAIL")
            return(False)
        
    def set_timeout(self, time_ms):
        self.timeout = time_ms
        self.inst.timeout = self.timeout
    
    def enable_sensing(self):
        self.inst.write(":INP ON")
    
    def get_current(self):
        print(self.inst.query(":MEAS:CURR?"))
        
    def set_speed(self, time_s):
        self.inst.write(":SENS:CURR:APER "+str(time_s))
    
    def set_range(self, curr_amp):
        self.inst.write(":SENS:CURR:RANG "+srt(curr_amp))
        
    def set_output_voltage(self, volt):
        self.inst.write(":SOUR:VOLT "+str(volt))
        
    def stop_output_voltage(self):
        self.inst.write(":OUTP OFF")
        
    def get_temperature(self):
        print(self.inst.query(":MEAS:TEMP?"))
        
#    def main():
#        inst = keysight()
#        inst.enable_sensing()
#        inst.get_current()
#        inst.get_temperature()
#        
#    if __name__ == '__main__':
#        main()
