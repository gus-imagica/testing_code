# -*- coding: utf-8 -*-
"""
Created on Wed May 17 09:45:11 2017

This function is useful for quickly setting the output of the Labjack DAC or
testing any of its other functions.

@author: Gus
"""

from labjackU3LV import Labjack
import time

# initialize
d = Labjack()
# display what is happening or not...
# d.u.debug = True

print(d.set_voltage(0, DAC = 0, is16bits = True))

#time.sleep(1)
#
#print(d.set_counter(reset = True))

#print(d.get_period())

#print(d.get_frequency(3))
## set the digital output to select direction.
#d.set_DO(6,1)
## Set the speed. The motor is active low so a high duty cycle is slower.
#d.set_pwm(0.5, pin = 4)
#time.sleep(5)
#
## Reverse direction
#d.set_DO(6,0)
#time.sleep(5)



d.close()