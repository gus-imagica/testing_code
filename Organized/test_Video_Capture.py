# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 15:01:02 2017

This code tests if a camera working by running a video feed.

@author: Gus
"""

import cv2

camera = cv2.VideoCapture(1)
if camera.isOpened():
    print("Camera connected")
    
properties = [cv2.CAP_PROP_APERTURE, cv2.CAP_PROP_EXPOSURE, cv2.CAP_PROP_FPS, cv2.CAP_PROP_CONTRAST]
names = ["Aperature: ", "Exposure: ", "FPS: ", "Contrast: "]

for ind, prop in enumerate(properties):
    p = camera.get(prop)
    print(names[ind], p)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1944)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 2592)

rval, frame = camera.read()

print(rval, frame.shape)

while rval:
    cv2.imshow("preview", frame)
    rval, frame = camera.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    if key == ord("p"):
        cv2.imwrite("tilt_image.jpg", frame)

camera.release()