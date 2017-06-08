# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:20:31 2017

This function finds the photodiode current at a particular TLS wavelength and 
filter setting and converts it to power and photon intensity values.

@author: Gus
"""

import matplotlib.pyplot as plt
import numpy as np
from newportTLS import TLS
from keysight import Keysight
from photodiode_calibration import diodeCal
import time

"""
Settings
"""

bias_voltage = 5.0

max_amps = 2e-10

auto_range = False

TLS_lam = 500

TLS_filter = 3

"""
Code
"""

keys = Keysight()

newp = TLS()

try:
    """ Initialize """
    # Initilize SMU
    keys.set_output_voltage(bias_voltage) # Bit of an arbitrary choice. Shouldn't matter much.
    newp.filterW(TLS_filter)
    newp.set_lambda(TLS_lam)
    
    diode = diodeCal()
    
    """ Set range """
    
    if auto_range:
        curr = 0
        while curr < max_amps*0.8: # dynamic range adjustment, make sure it isn't overflowing
            keys.set_range(max_amps)
            curr = keys.get_current()
            max_amps *= 0.1
    else:
        keys.set_range(max_amps)
        time.sleep(1)
        curr = keys.get_current()
    
    temp = keys.get_temperature()
    dark_current = diode.dark(temp)
    
    print("Total current: ", curr, " Amps")
        
    
    light_curr = curr - dark_current
    
    print("Light induced current: ",light_curr," Amps")
    
    pd_cal = diode.func # amps per watts conversion factor
    power_W = light_curr/pd_cal(TLS_lam) # power from light conversion
    print("Power: ",power_W," Watts")
    
    intensity = power_W/diode.area
    print("Intensity: ",intensity," W/m**2")
    
    """ Convert power to photons """
    hc = 1.98644568e-16 # J nm
    photon_J = hc/TLS_lam 
    photons_persec = power_W/photon_J # photon current on the photodiode
    photon_intensity = intensity/photon_J
    print("Photon intensity: ", photon_intensity, "photons/m**2/s")
    
    """ Check Photodiode QE """
    e_per_coulomb = 6.242e18 # convert amps to electron flow
    electron_charge = 1.60217662e-19
    
    pd_QE = light_curr*e_per_coulomb/photons_persec
    print("Photodiode QE (electrons per photon): ", pd_QE)
    expected_QE = pd_cal(TLS_lam)*photon_J/electron_charge
    
    print("Temperature: ", temp," Celcius")
    
    print("Predicted dark current: ", diode.dark(temp), " Amps")
    
except Exception as e:
    keys.close()
    newp.close()
    raise e
# keys.close()
newp.close()