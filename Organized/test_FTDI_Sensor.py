# -*- coding: utf-8 -*-
"""
Created on Thu May 11 16:09:46 2017

This function captures a single frame from the Sony sensor and plots it.
Changing the aperature time affects the output of the sensor. Changing the
number of repetitions changes the number of frames plotted.


@author: Gus
"""

from _FTDI_Sensor import sensor

import matplotlib.pyplot as plt
import numpy as np

""" Settings """
frames = 1
integ_time = 1

""" Initialize """
sens = sensor(port = "COM7", print_out = False)

try:    
    sens.set_aper(integ_time)
    sens.set_reps(1)
    plt.figure(figsize = (12, 7))
    
    array = []
    for i in range(frames):
        frame = sens.get_spect()
        array.append(frame)
        plt.plot(frame, ".", linewidth = 0.5, ms = 1.5)
        print(np.mean(array), " mean, ", np.median(array), " median.")
        
    if frames>1:
        plt.plot(np.std(array, 0)*50, linewidth = 0.5)
        
    plt.show()
    
#    plt.figure(figsize = (12, 7))
#    plt.plot(array[0:300])
#    plt.show()
    
    sens.close()
except Exception as e:
    sens.close()
    raise e