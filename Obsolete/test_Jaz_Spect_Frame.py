# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:03:13 2017

This function plots a spectrum from the Jaz spectrometer.

@author: Gus
"""

from newportTLS import TLS
from jazSpect import Spect

newp_con = True

if newp_con:
    newp = TLS()
    
    newp.set_lambda(760)
    
    filterW = 3
    
    newp.filterW(filterW)

else: filterW = None

int_time = 1000

jaz = Spect(int_time = int_time)

intens = jaz.get_intensities()

jaz.plot(intens, int_time = int_time, filterW = filterW)

jaz.plot(intens, rang = 200)

jaz.close()

if newp_con:
    newp.close()