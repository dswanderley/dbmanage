# -*- coding: utf-8 -*-
"""
Created on Wed Jul 03 17:16:20 2019

@author: Diego Wanderley
@python: 3.6
@description: Verify if an image has annotations
"""

import os
import numpy as np
#import matplotlib.pyplot as plt
from PIL import Image

data_path = "//192.168.106.134/Diego Wanderley/Ultrasonix/organized/Data"
fname = 'pat_0_20190410_115421.png'#'pat_A4_20180301_110708.png'#'pat_0_20190429_094726.png'

# Color values
c_point_alt = [0,252,54]
c_point = [0,255,0]
c_measure = [0,255,255]
c_auto = [150,150,150]
c_yinfo = [210,210,0]

# Get images
pnglist = [f for f in os.listdir(data_path) if f.endswith('.png')]
# Read images
for fname in pnglist:
    # Set path
    path_png = os.path.join(data_path, fname)
    # Read Image
    img = Image.open(path_png).convert("RGB")
    img_np = np.array(img)
    # Set FOV
    fov = img_np[100:700, 80:680, :]

    # Get indexes
    i_point_alt = np.where(np.all(fov == c_point_alt, axis=-1))
    i_point = np.where(np.all(fov == c_point, axis=-1))
    i_measure = np.where(np.all(fov == c_measure, axis=-1))
    i_auto = np.where(np.all(fov == c_auto, axis=-1))
    i_yinfo = np.where(np.all(fov == c_yinfo, axis=-1))
    
    marks = "empty"
    if (len(i_point[0]) > 0 or len(i_point_alt[0]) > 0):
        # has point
        marks = "point"
        if (len(i_measure[0]) > 0):
            # has measurements
            marks = "measurements"
            if ((len(i_auto[0]) > 0) and (len(i_yinfo[0]) > 0)):
                # has autofolicle
                marks = "auto_follicle"
                #print(fname)
                                
    #imgplot = plt.imshow(fov)
    #plt.show()
    #print(marks)