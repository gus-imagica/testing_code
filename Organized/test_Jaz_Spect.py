# -*- coding: utf-8 -*-
"""
Spyder Editor

This script continuously plots the output of the Jaz Spectrometer.

This is a temporary script file.
"""

from _Jaz_Spectrometer import Spect

import matplotlib.pyplot as plt
import numpy as np

""" Settings """

sub_range = 100

continuous = True

""" Initialize """

jaz = Spect()

wavelengths = jaz.wavelengths



if sub_range is not None:
    twoplots = True
else:
    twoplots = False

fig = plt.figure(figsize = (12, 9))

if twoplots:
    graph1 = fig.add_subplot(1,2,1)
    graph2 = fig.add_subplot(1,2,2)
    graph2.set_ylabel('intensity')
    graph2.set_xlabel('wavelength (nm)')
    graph1.set_ylabel('intensity')
    graph1.set_xlabel('wavelength (nm)')
else:
    graph1 = fig.add_subplot(1,1,1)
    graph1.set_ylabel("intensity")
    
title = "Intensity Spectrum"

fig.suptitle(title)

intens = jaz.get_intensities()

graph1.plot(wavelengths,intens)
plt.ion()
plt.show()

plt.draw()
plt.pause(0.01)

cont = True
while cont:
    cont = continuous
    try: 
        intens = jaz.get_intensities()
        
        index_max = np.argmax(intens)
        
        if twoplots:
            upper = sub_range
            lower = sub_range
            
            if index_max+upper > len(wavelengths):
                upper = len(wavelengths)-index_max-1
            if index_max-lower < 0:
                lower = index_max
            
            close_int = intens[index_max-lower:index_max+upper]
            close_wav = wavelengths[index_max-lower:index_max+upper]
            
            graph2.clear()
            graph2.plot(close_wav, close_int)
            
        graph1.clear()
        graph1.plot(wavelengths, intens)
        # graph1.set_ydata(intens)
            
        plt.draw()
        plt.pause(0.01)
        # time.sleep(0.25)

    except KeyboardInterrupt:
        jaz.close()
        break
jaz.close()