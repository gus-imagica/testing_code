# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 15:01:02 2017

@author: Gus
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

frame = cv2.imread("target1.png")

cv2.imshow("Target", frame)

gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

line = gray_frame[200,:]
plt.plot(line)

highs = np.array([], dtype = int)
lows = np.array([], dtype = int)
y_last = 255
mid = 256/2
up_x = 0
down_x = 0
for x, y in enumerate(line):
    if y > mid and y_last > mid:
        pass
    if y < mid and y_last < mid:
        pass
    if y > mid and y_last < mid:
        up_x = x
        if down_x:
            lows = np.append(lows, int((down_x+up_x)/2))
    if y < mid and y_last > mid:
        down_x = x
        if up_x:
            highs = np.append(highs, int((down_x+up_x)/2))
    y_last = y

high_y = 255*np.ones_like(highs)
low_y = np.zeros_like(lows)

plt.plot(highs,high_y,"o")
plt.plot(lows,low_y,"x")
        

blur = cv2.GaussianBlur(gray_frame, (5,5), 4)
cv2.imshow("Blur", blur)

blur_line = blur[200,:]
blur_line = np.int16(blur_line)
plt.plot(blur_line)

comp = np.divide((blur_line[list(highs)]-blur_line[list(lows)]), blur_line[list(highs)])
plt.plot(highs, 100*comp, lw = 5)
