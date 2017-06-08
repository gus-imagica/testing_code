# -*- coding: utf-8 -*-
"""
Created on Fri May 19 12:11:58 2017

@author: Gus
"""

from scipy import stats
import matplotlib.pyplot as plt

time = [10, 15, 20, 25, 35, 50, 75, 100]
volt = [0.29, 0.322, 0.37, 0.42, 0.51, 0.648, 0.88, 1.06]
level = [200, 311, 440, 615, 880, 1250, 1921, 2549]

plt.figure()
plt.plot(volt, level)
plt.xlabel("output voltage difference")
plt.ylabel("output levels")
plt.figure()
plt.plot(time, level)
plt.xlabel("integration time ms")
plt.ylabel("output levels")
plt.figure()
plt.plot(time, volt)
plt.xlabel("integration time ms")
plt.ylabel("output voltage difference")
plt.show()

print(stats.linregress(time, level))

print(stats.linregress(level, volt))