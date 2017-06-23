# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 15:01:02 2017

This code tests if a camera working by running a video feed.

@author: Gus
"""

import cv2
import os

camera = cv2.VideoCapture(1)
if camera.isOpened():
    print("Camera connected")
    
properties = [cv2.CAP_PROP_APERTURE, cv2.CAP_PROP_EXPOSURE, cv2.CAP_PROP_FPS, cv2.CAP_PROP_CONTRAST]
names = ["Aperature: ", "Exposure: ", "FPS: ", "Contrast: "]

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1944)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 2592)

rval, frame = camera.read()

print(rval, frame.shape)

while rval:
    rval, frame = camera.read()
    small= cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)
    cv2.imshow("preview", small)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    if key == ord("p"):
        file_path = "vid_image%s.jpg"
        number = 0
        while os.path.exists(file_path % number):
            number += 1
        cv2.imwrite(file_path % number, frame)
        print(file_path % number)
    if key == ord("q"):
        for ind, prop in enumerate(properties):
            p = camera.get(prop)
            print(names[ind], p)
    elif key is not 255:
        print("key: ", key, " char: ", chr(key))
        
camera.release()