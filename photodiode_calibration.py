# -*- coding: utf-8 -*-
"""
Created on Wed May 10 17:08:00 2017

@author: Gus
"""

from scipy.interpolate import interp1d as interp
import numpy as np

class diodeCal(object):
    def __init__(self, filepath = "C:/Users/Gus/Google Drive/Testing/Equipment/Photodiodes/PhotodiodeCal.txt"):
        cal_file = open(filepath, 'r')
        
        result = []
        lams = []
        effs = []
        for line in cal_file.readlines()[1:]:
            strlist = line.split('\t')
            lam = float(strlist[0])
            eff = float(strlist[1])
            result.append([lam, eff])
            lams.append(lam)
            effs.append(eff)
        
        cal_file.close()
        
        result = np.array(result)
        
        self.array = result
        self.lambdas = lams
        self.effic = effs
        
        self.area = 13e-6 # 13 mm squared
        
        self.func = interp(lams, effs, kind = "cubic")
        
        # make this into a function that can interpolate any point in the spectrum