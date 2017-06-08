# -*- coding: utf-8 -*-
"""
Created on Wed May 17 09:24:42 2017

@author: Gus

Configures the Labjack DAC.
FIO4: Timer 0, produces a 26785.7 Hz PWM signal with adjustable duty cycle.
FIO5: Timer 1, input for motor encoder, records the period of a square wave input.
FIO6: Counter 1, counts spikes - possibly useful but not needed.

DAC0/1: Configurable analog voltage outputs

FIO0-3: Available for DIO using set_DO and get_DI

"""

import u3
import time

class Labjack(object):
    
    def __init__ (self,):
        self.u = u3.U3()
        self.u.getCalibrationData()
        self.clockSpeed = 48e6 # 48 MHz
        self.clockDivisor = 7 # gets the correct PWM output
        self.u.configIO(NumberOfTimersEnabled=2, EnableCounter1=1, TimerCounterPinOffset = 4)
        self.u.getFeedback(u3.TimerConfig(timer = 1, TimerMode=3))
        self.u.getFeedback(u3.TimerConfig(timer = 0, TimerMode=1, Value=0))
        # self.u.configTimerClock(TimerClockBase=6, TimerClockDivisor=7) # 187500/7 = 26785.7 Hz
        self.u.configTimerClock(TimerClockBase=2) # needed for smooth 
        
    def set_voltage(self, voltage, DAC = 0, is16bits = True):
        setbits = self.u.voltageToDACBits(voltage, is16Bits = is16bits)
        if is16bits:
            self.u.getFeedback(u3.DAC16(Dac = DAC, Value = setbits))
            binary = bin(setbits)[2:].zfill(16)
            actualV = int(binary[:10],2)/(2**10)*(4.95-0.04)+0.04
            # print(actualV)
            return actualV
        else:
            self.u.getFeedback(u3.DAC8(Dac = DAC, Value = setbits))
            binary = bin(setbits)[2:].zfill(8)
            actualV = int(binary[:8],2)/(2**8)*(4.95-0.04)+0.04
            # print(actualV)
            return actualV
        
    def set_pwm(self, duty):        
        set_bits = 65536-int(duty*65536)
        self.u.getFeedback(u3.TimerConfig(timer = 0, TimerMode=1, Value=set_bits))
        
    def update_pwm(self, duty):
        set_bits = 65536-int(duty*65536)
        self.u.getFeedback(u3.Timer0(Value=set_bits, UpdateReset=True))
        
    def set_LED(self, state = 1):
        self.u.getFeedback(u3.LED(State = state))
    
    def __readAllDIO(self):
        return self.u.getFeedback(u3.PortStateRead())
    
    def set_DO(self, ioNum, state):
        return self.u.setDOState(ioNum = ioNum, state = state)
        
    def get_DI(self, ioNum):
        return self.u.getDIState(ioNum = ioNum)
    
    def getTemp(self):
        tempK = self.u.getTemperature()
        tempC = tempK-273.15
        return tempC
    
    def set_counter(self, reset = False):
        return self.u.getFeedback(u3.Counter(counter = 1, Reset = reset))
        
    def get_period(self, maximum_s):
        time.sleep(maximum_s*1.5)
        bits = self.u.getFeedback(u3.Timer(timer = 1))
        period = bits[0]/self.clockSpeed*self.clockDivisor
        return period
    
    def get_frequency(self, minimum_Hz):
        maximum_s = 1.0/minimum_Hz
        period = self.get_period(maximum_s)
        frequency = 1.0/period
        # Seems to be about 0.9975 of the actual value.
        return frequency
    
    def __ToggleLED(self):
        self.u.toggleLED()
    
    def close(self):
        self.u.close()