# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:27:25 2017

@author: Gus
"""

import cv2
import numpy as np

img1 =  cv2.imread("C:/Users/Gus/Documents/GitHub/testing_code/target2.PNG")
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
print(img1.shape)

img2 = cv2.imread("C:/Users/Gus/Documents/GitHub/testing_code/vid_image0.jpg")
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
print(img2.shape)

""" matchTemplate method """

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
methods = ['cv2.TM_CCORR_NORMED']

scales = [0.2, 0.5, 1, 1.5, 2]
# scales = [0.5]

best_max = 0

for scale in scales:
    resiz = cv2.resize(img1, (0,0), fx = scale, fy = scale)
    # Step 2: Get the size of the template. This is the same size as the match.
    trows,tcols = resiz.shape[:2]
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
    
        result = cv2.matchTemplate(resiz, img, method)
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            print(meth, " ", min_val)
            MPx,MPy = min_loc
        else:
            print(meth, " ", max_val)
            MPx,MPy = max_loc
        
        # Step 3: Draw the rectangle on large_image
        cv2.rectangle(img2, (MPx,MPy),(MPx+tcols,MPy+trows),(0,0,255),2)
        cv2.putText(img2, meth, (MPx,MPy+trows), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
        
small= cv2.resize(img2, (0,0), fx = 0.5, fy = 0.5)

cv2.imshow("Matches", small)


""" This brute force method did not work well. """
#orb = cv2.ORB_create()
#
#kp1, des1 = orb.detectAndCompute(img1,None)
#kp2, des2 = orb.detectAndCompute(img2,None)
#
#bf = cv2.BFMatcher(cv2.NORM_HAMMING2,crossCheck=True)
#
## Match descriptors.
#matches = bf.match(des1,des2)
#
## Sort them in the order of their distance.
#matches = sorted(matches, key = lambda x:x.distance)
#
## Draw first 10 matches.
#img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10], None, flags=2)
#
#small= cv2.resize(img3, (0,0), fx = 0.5, fy = 0.5)
#
#cv2.imshow("Matches", small)

""" FLANN Algorithm """
#orb = cv2.ORB_create()
#
#kp1, des1 = orb.detectAndCompute(img1,None)
#kp2, des2 = orb.detectAndCompute(img2,None)
#
## FLANN parameters
#FLANN_INDEX_KDTREE = 0
#index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#search_params = dict(checks=50)   # or pass empty dictionary
#
#flann = cv2.FlannBasedMatcher(index_params,search_params)
#
#matches = flann.knnMatch(des1,des2,k=2)
#
## Need to draw only good matches, so create a mask
#matchesMask = [[0,0] for i in range(len(matches))]
#
## ratio test as per Lowe's paper
#for i,(m,n) in enumerate(matches):
#    if m.distance < 0.7*n.distance:
#        matchesMask[i]=[1,0]
#
#draw_params = dict(matchColor = (0,255,0),
#                   singlePointColor = (255,0,0),
#                   matchesMask = matchesMask,
#                   flags = 0)
#
#img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
#
#small= cv2.resize(img3, (0,0), fx = 0.5, fy = 0.5)
#
#cv2.imshow("Matches", small)