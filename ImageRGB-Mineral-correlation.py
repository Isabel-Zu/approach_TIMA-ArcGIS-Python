# -*- coding: utf-8 -*-
"""
This script uses TIMA Phase images to create a csv table with the Mineralname and 
its x|y position in the image based on the RGB value. The TIMA phases images are 
color coded by a specific colormap, which needs to be exported beforehand as a 
textfile with following content and format: [Mineralname R-value G-value B-value].
 
WORKFLOW:
    1. Load image and colormap-txtfile (RGB values defining minerals)
    2. Iterate over the whole image to get the RGB value for each pixel point (x,y).
       Mineral-name and related x|y value are stored, if the RGB value is identical 
       to one of the colormap.
    3. Output Table: X, Y, Mineral

USER INPUT:
    Image - Location\filename.tif (line 37)
    Colormap - Location\filename.txt (line 39)
    Storage - Location\filename.csv (line 85)
    
Created:  16/06/2020
Last modified: 25/05/2021
Author:   Isabel Zutterkirch
"""

#-----------------------------------------------------------------------------
## USED MODULS

import cv2
import csv
import pandas as pd
import numpy as np

#-----------------------------------------------------------------------------
## INPUT

# image
image= cv2.imread(r'C:\foldername\imagename.tif')
# colormap-list [Mineralname R-value G-value B-value]
colors= pd.read_csv(r'C:\foldername\imagecolors.txt',sep=' ')

#-----------------------------------------------------------------------------
## PROCESSING

# create color dictionary
dictionary={}
with open (r'C:\foldername\imagecolors.txt') as g:
    next(g)
    for line in g:
        (mineralname, valR, valG, valB)= line.split()
        dictionary[(int(valR), int(valG), int(valB))]= str(mineralname)
        
# iteration
# get image shape/dimensions
height,width,channels=image.shape                               
# create empty lists to store values
xls=[]
yls=[]
mineral=[]
# iterate over height, width and colors
for y in range(height):
    for x in range (width):
        b=image[y][x][0]
        g=image[y][x][1]
        r=image[y][x][2]
        rgb= (r,g,b)
        value = dictionary.get(rgb)
        if value is not None:
            mineral.append(value)
            xls.append(x)
            yls.append(y)
        else:
            mineral.append('unrecognized')
            xls.append(x)
            yls.append(y)

# reverse the y values for the output table format
yls_inv=yls.reverse()
# combine the arrays        
rows= zip(yls,xls,mineral)  

#-----------------------------------------------------------------------------
## OUTPUT

# name storage locations and filename      
newfilePath1= r'C:\foldername\filename.csv'
with open(newfilePath1, "wb") as f:
    writer= csv.writer(f)
    for row in rows:
        writer.writerow(row)
