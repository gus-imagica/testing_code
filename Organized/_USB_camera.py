# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 11:47:59 2017

@author: Gus
"""

from cv2 import VideoCapture

class cam(VideoCapture):
    def __init__(self, cam_number, width, height):
        cv2.VideoCapture.__init__(self, cam_number)
        self.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.set(cv2.CAP_PROP_FRAME_HEIGTH, height)