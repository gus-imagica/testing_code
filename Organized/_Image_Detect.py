# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 16:42:38 2017

This method detects a region within an image on which to perform MTF analysis.

@author: Gus
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

""" Settings """
target_path_vert = "C:/Users/Gus/Documents/GitHub/testing_code/target2.PNG"
image_path = "C:/Users/Gus/Documents/GitHub/testing_code/vid_image2.jpg"
# image_path = "C:/Users/Gus/Documents/GitHub/testing_code/target2.PNG"

def TEST():
    vertical = True
    pixel_pitch_mm = 2.2/1000
    raw_image = cv2.imread(image_path)
    grey_image = grey_img(raw_image)
    target_coords = find_target(grey_image, vert = vertical, display = True)
    roi = grab_roi(target_coords[0],target_coords[1],grey_image)
    # cv2.imshow("ROI", roi)
    upline, downline = grab_line(roi, vert = vertical)
    MTF_curve(upline, pixel_pitch_mm)
    
def find_target(grey_image, vert = True, num_scales = 10, display = False):
    templ = cv2.imread(target_path_vert)
    templ = cv2.cvtColor(templ, cv2.COLOR_BGR2GRAY)
    if not vert:
        templ = cv2.transpose(templ)
        templ = cv2.flip(templ,1)
    
    img2 = grey_image

    method = cv2.TM_CCORR_NORMED
    
    scales = np.geomspace(0.1,10,num_scales)
    
    best_max = 0
    best_match = None
    
    for scale in scales:
        resiz = cv2.resize(templ, (0,0), fx = scale, fy = scale)
        
        if resiz.shape[0] > img2.shape[0] or resiz.shape[1] > img2.shape[1]:
            continue
        # Step 2: Get the size of the template. This is the same size as the match.
        trows,tcols = resiz.shape[:2]

        img = img2.copy()
    
        result = cv2.matchTemplate(resiz, img, method)
        
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            MPx,MPy = min_loc
        else:
            MPx,MPy = max_loc
            
        if max_val > best_max:
            best_max = max_val
            best_match = [(MPx,MPy),(MPx+tcols,MPy+trows)]
        
    if best_match is None:
        return None
    
    # Step 3: Draw the rectangle on large_image
    cv2.rectangle(img2, best_match[0], best_match[1],(0,0,255),2)
            
    small= cv2.resize(img2, (0,0), fx = 0.5, fy = 0.5)
    
    if display:
        cv2.imshow("Matches", small)
    
    return best_match

def grey_img(image):
    if len(image.shape) is 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        return image

def grab_roi(corner1, corner2, grey_image):
    x1 = corner1[1]
    y1 = corner1[0]
    x2 = corner2[1]
    y2 = corner2[0]
    if x2>x1 and y2>y1:
        return grey_image[x1:x2,y1:y2]
    if x2>x1 and not y2>y1:
        return grey_image[x1:x2,y2:y1]
    if not x2>x1 and y2>y1:
        return grey_image[x2:x1,y1:y2]
    else:
        return grey_image[x2:x1,y2:y1]
    
def grab_line(roi_image, vert = True):
    # trim ROI to only include the tilted thing
    L,W = roi_image.shape
    roi_image = roi_image[int(0.2*L):int(0.8*L),int(0.2*W):int(0.8*W)]
    #cv2.imshow("trimmed ROI", roi_image)
    
    if vert:
        roi_image = cv2.transpose(roi_image)
        
    sums = np.sum(roi_image, 1)
    sums = sums.astype(float)
    norm_sums = (sums-min(sums))/(max(sums)-min(sums))
    norm_diff = np.ediff1d(norm_sums)
    
    # find the points closest to half way
    inds = (np.abs(norm_sums-0.5)).argsort()
    
    upline = None
    downline = None
    
    for ind in inds:
        if upline is not None and downline is not None:
            break
        if upline is None:
            if norm_diff[ind] > 0:
                upline = roi_image[ind,:]
        if downline is None:
            if norm_diff[ind] < 0:
                downline = roi_image[ind,:]

#    plt.plot(norm_sums)
#    plt.figure()
#    plt.plot(norm_diff)
#    plt.figure()
#    plt.plot(upline)
#    plt.plot(downline)
#    plt.show()
    return upline, downline
    
def MTF_curve(line, pixel_pitch_mm):
    sfr = line
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

if __name__ == "__main__":
    sums = TEST()