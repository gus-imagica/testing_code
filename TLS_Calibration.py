# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:03:13 2017

@author: Gus
"""

from newportTLS import TLS
from jazSpect import Spect

newp = TLS()

newp.set_lambda(500)

jaz = Spect(int_time = 3000)

intens = jaz.get_intensities()

jaz.plot(intens)

jaz.plot(intens, 50)

jaz.close()

newp.close()