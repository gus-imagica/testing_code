# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 09:03:43 2017

@author: Gus
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

"""
Settings
"""
#roi_horz = slice(100,250)
#roi_vert = slice(100,250)
#image = "target2.png"
#pixel_pitch = None

roi_horz = slice(910,1100)
roi_vert = slice(0,250)
image = "organized/tilt_image.jpg"
pixel_pitch_mm = 2.2/1000

"""
Code
"""

frame = cv2.imread(image)
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Target", gray_frame)

roi = gray_frame[roi_vert, roi_horz]
cv2.imshow("roi",roi)

def find_mid_ind(iterable):
    it = iterable - min(iterable) # somewhat normalized
    av = np.mean(it)
    ind = (np.abs(it-av)).argmin()
    return ind

flat = np.sum(roi, 0)
sfr = roi[:,find_mid_ind(flat)]
sfr = sfr.astype(float)
sfr = sfr/max(sfr)
plt.figure("sfr")
plt.plot(sfr)

lsf = np.diff(sfr)
# lsf = np.absolute(lsf)
plt.plot(lsf)

mtf = np.absolute(np.fft.fft(lsf))
freq = np.fft.fftfreq(mtf.shape[0])
spac_freq = freq/pixel_pitch_mm
mtf = mtf[freq>0]
spac_freq = spac_freq[freq>0]
plt.figure("mtf")
plt.plot(spac_freq,mtf)
plt.xlabel("cycles/mm")

#blur = cv2.GaussianBlur(roi, (5,5), 4)
#cv2.imshow("Blur", blur)
#
#sfr = np.int16(blur[:,74])
#plt.figure("sfr")
#plt.plot(sfr)
#
#lsf = np.diff(sfr)
#lsf = np.absolute(lsf)
#plt.plot(lsf)
#
#mtf = np.absolute(np.fft.fft(lsf))
#freq = np.fft.fftfreq(mtf.shape[0])
#mtf = mtf[freq>0]
#freq = freq[freq>0]
#plt.figure("mtf")
#plt.plot(freq,mtf)
