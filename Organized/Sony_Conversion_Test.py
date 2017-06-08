# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:31:50 2017

This function computes the conversion coefficient (uv/electron)
for the Sony sensor, using an estimated value of QE.

@author: Gus
"""

from _Newport_TLS import TLS
from _FTDI_Sensor import sensor
from _Photodiode_Cal import diodeCal
from _Keysight_SMU import Keysight

import matplotlib.pyplot as plt
import numpy as np
import os
import time

"""
Settings
"""

bias_voltage = 5
# dark_current = 4.24e-11 # at 5V bias

peak_lam = 555 # maximum value of lux
lux_perWmm = 683.002 # conversion factor

aper_time = 0.5

integ_ms = 2000
integ_offset = 4.3 # this is how many milliseconds the integration takes if the time is set to 0.

filterW = 1 # Wheel 1 is no filter

auto_range = False
max_amps = 2e-10

save_file = False

file_suffix = "diffuser"

"""
Code
"""

sens = sensor(port = "COM6", print_out = False)

newp = TLS()

keys = Keysight()

try:
    """ Initialize """
    # Initilize SMU
    keys.set_output_voltage(bias_voltage) # Bit of an arbitrary choice. Shouldn't matter much.
    newp.filterW(filterW)
    keys.set_aper(aper_time)
    
    # Initialize TLS
    newp.set_lambda(peak_lam)
    TLS_lam = newp.get_lambda()
    print("Wavelength: ",TLS_lam)
    
    # Initialize sensor
    sens.set_aper(integ_ms)
    sens.set_reps(5)
    
    diode = diodeCal()
    
    """ Get current """
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
    print("Temperature: "+str(temp))
    dark_current = diode.dark(temp)
#    dark_current = 3.5775e-11
    print("Dark current: ", dark_current)
    
    print("Total current: ", curr, " Amps")
    light_curr = curr - dark_current
    print("Light induced current: ",light_curr," Amps")
    
    """ Convert current to power """
    
    diode.func # amps per watts conversion factor
    power_W = light_curr/diode.func(TLS_lam) # power coming from the photodiode
    
    """ Convert power to photons """
    hc = 1.98644568e-16 # J nm
    photon_J = hc/TLS_lam 
    photons_persec = power_W/photon_J # photon current on the photodiode
    photon_intensity = photons_persec/diode.area
    print("Photon intensity (m-2 s-1): ", photon_intensity)
    
    """ Check Photodiode QE """
    e_per_coulomb = 6.242e18 # convert amps to electron flow
    
    pd_QE = light_curr*e_per_coulomb/photons_persec
    print("Photodiode QE (electrons per photon): ", pd_QE)
    
    """ Read sensor """
    print("\n Reading Sony Sensor... \n")
    array = sens.get_spect()
    
    plt.figure(figsize = (12, 7))
    plt.plot(array)
    plt.show()
    
    av_level = np.mean(array[1100:1200])
    print("Average sensor level: ", av_level)
    
    av_voltage = av_level*0.0003343+0.221-0.17 # 0.17 is the dark voltage, 0.221 is the minimum voltage for readout, 0.000334 is the best fit slope
    print("Average sensor voltage: ", av_voltage)
    
    pixel_area = 14*56e-12 # meters squared
    exposure_ms = integ_ms + integ_offset # the way the sensor works
    
    """ Check sensitivity """
    lux = power_W/diode.area*lux_perWmm
    lux_s = lux*0.001*exposure_ms
    volt_perluxs = av_voltage/lux_s
    print("sensitivity (V/lux.s): ", volt_perluxs)
    
    photons = pixel_area*exposure_ms*0.001*photon_intensity
    
    print("Efficiency (uV/photon): ", av_voltage/photons*1000000)
    
    QE = 0.25 # This is a guess! 
    print("Estimated QE: ",QE*100,"%")
    
    electrons = QE*photons
    
    efficiency = av_voltage/electrons # Volt per electron
    
    print("Efficiency (uV/electron): ", efficiency*1000000) # microvolt per electron
    
    if save_file:
        file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
        file_path = file_base+"/TLS_intensity_"+file_suffix+"%s.txt"
        number = 1
        while os.path.exists(file_path % number):
            number += 1
            
        f = open(file_path % number, "wb")
        
        head = "wavelength_nm, curr_A, power_W, Temperature = %s" % temp
        np.savetxt(f, (TLS_lam, curr_av, watts), header = head, delimiter = "\t") 
        
        f.close()
        
        data = np.loadtxt(file_path % number, unpack=True)
        lambda_nm = data[:,0] 
        curr_A = data[:,1]
        power_W = data[:,0]
except Exception as e:
    keys.close()
    newp.close()
    sens.close()
    raise e
    
keys.close()
newp.close()
sens.close()