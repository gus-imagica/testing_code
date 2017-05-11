# -*- coding: utf-8 -*-
"""
Created on Tue May  2 14:05:22 2017

@author: Gus
"""

import visa

class Keysight(object):
    
    def __init__(self, self_cal = False, self_test = False, timeout_ms = 5000, default_connection = 0):
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
        self.enable_output_voltage()
        self.enable_sensing()
        
    
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
        
    def set_display(self, ON):
        if ON:
            self.inst.write(":DISP:ENAB ON")
        else:
            self.inst.write(":DISP:ENAB OFF")
    
    def enable_sensing(self):
        self.inst.write(":INP ON")
    
    def get_current(self):
        try:
            curr = float(self.inst.query(":MEAS:CURR?"))
        except Exception:
            curr = None
        return curr
        
    def set_speed(self, time_s):
        self.inst.write(":SENS:CURR:APER "+str(time_s))
    
    def set_range(self, curr_amp):
        self.inst.write(":SENS:CURR:RANG "+str(curr_amp))
        
    def enable_output_voltage(self):
        self.inst.write(":OUTP ON")
        
    def set_output_voltage(self, volt):
        if volt < 20 and volt >= 0: # Limited for the photodiode opperation
            self.inst.write(":SOUR:VOLT "+str(volt))
        
    def stop_output_voltage(self):
        self.inst.write(":OUTP OFF")
        
    def get_temperature(self):
        try:
            temp = float(self.inst.query(":SYST:TEMP?"))
        except Exception:
            temp = None
        return temp
    
    def set_aper(self, time_ms):
        self.inst.write(":SENS:CURR:APER "+str(time_ms))
        
    def auto_aper(self, ON):
        self.inst.write(":SENS:CURR:APER:AUTO "+str(ON))
        
    def get_aper(self):
        try:
            temp = float(self.inst.query(":SENS:CURR:APER?"))
        except Exception:
            temp = None
        return temp
    
    # returns temperature and current measurements for each of the voltages
    def current_test(self, voltages, curr_range = 2E-6, measure_temp = True, aper_time_s = None):
        self.set_range(curr_range)
        
        if aper_time_s is not None:
            self.auto_aper(False)
            self.set_aper(aper_time_s)
        else:
            self.auto_aper(True)
            
        data = []
        for volt in voltages:
            self.set_output_voltage(volt)
            datum = [self.get_current()]
            if measure_temp:
                temp = self.get_temperature()
                datum.append(temp)
            data.append(datum)
        return data
    
    def close(self):
        self.inst.close()

#    def main():
#        inst = keysight()
#        inst.enable_sensing()
#        inst.get_current()
#        inst.get_temperature()
#        
#    if __name__ == '__main__':
#        main()
