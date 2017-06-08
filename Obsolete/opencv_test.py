# -*- coding: utf-8 -*-
"""
Created on Mon May 29 16:29:35 2017

@author: Gus
"""

import opencv as cv2

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(0.01) & 0xFF == ord('q'):
        break