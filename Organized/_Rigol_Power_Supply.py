# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 13:46:20 2017

This class allows easy connection to a Rigol power supply and some functions
to set up the outputs.

@author: Gus
"""

import visa

class Rigol(object):
    
    def __init__(self, self_cal = False, self_test = False, timeout_ms = 10000, default_connection = 1):
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
        self.enable_ocp()
        self.enable_output_voltage()
        
    
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
        if "FAIL" in result:
            print("self-test FAIL")
            return(False)
        else:
            print("self-test PASS")
            return(True)
    
    # Overcurrent protection should be enabled. The default level is 3.3A
    def enable_ocp(self, chan = None):
        if chan is None:
            for c in [1,2,3]:
                self.inst.write(":OUTP:OCP CH%d,ON" % c)
        else:
            self.inst.write(":OUTP:OCP CH%d,ON" % chan)
    
    def set_timeout(self, time_ms):
        self.timeout = time_ms
        self.inst.timeout = self.timeout
        
    def enable_output_voltage(self, chan = None):
        if chan is None:
            for c in [1,2,3]:
                self.inst.write(":OUTP CH%d,ON" % c)
        else:
            self.inst.write(":OUTP CH%d,ON" % chan)
        
    def set_output_voltage(self, volt, chan = 1):
        self.inst.write(":APPL CH%d," % chan + str(volt))
        return self.inst.query(":APPL?")
        
    def stop_output_voltage(self, chan = None):
        if chan is None:
            for c in [1,2,3]:
                self.inst.write(":OUTP CH%d,OFF" % c)
        else:
            self.inst.write(":OUTP CH%d,OFF" % chan)
    
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
