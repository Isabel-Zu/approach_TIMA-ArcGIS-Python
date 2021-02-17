# -*- coding: utf-8 -*-
"""
This script uses TIMA Phase images, in which the phases are color coded by the 
Curtin Minerals colormap, and creates a csv table with x, y position from the 
image related to the Mineral based on the RGB value.

WORKFLOW:
    1. Load image and colormap (RGB values defining minerals)
    2. Loop over the whole image, get the RGB value at each pixel point (x,y),
        if the RGB value is same than that from the colormap list store the 
        mineral name and the related x,y values.
    3. Output Table: X, Y, Mineral

USER INPUT:
    Image - Location\filename (line 29)
    Storage - Location\filename (line 60)
    
Created:  16/06/2020
Modified: 17/06/2020
Author:   Isabel 
"""

import cv2
import csv
import pandas as pd
import numpy as np

##LOAD INPUT
#Image
image= cv2.imread(r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\data_large\2_ProcessedData\6_Further\2002584 R+T+CL_bw_mask_cut.tif')
#Colormap-List [Mineralname R-value G-value B-value]
#colors= pd.read_csv(r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\data_large\1_RawData\TIMA_CurtinMinerals_colors.txt',sep=' ')
colors= pd.read_csv(r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\data_large\1_RawData\Zr_ImageProcess_colors.txt',sep=' ')

## Create color dictionary
dictionary={}
with open (r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\data_large\1_RawData\Zr_ImageProcess_colors.txt') as g:
    next(g)
    for line in g:
        (mineralname, valR, valG, valB)= line.split()
        dictionary[(int(valR), int(valG), int(valB))]= str(mineralname)
        
##LOOP
#get image shape
height,width,channels=image.shape                               
#create empty lists to store values
xls=[]
yls=[]
mineral=[]
#loop over height, width and colors
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

##CREATE OUTPUT TABLE 
#reverse the y values
yls_inv=yls.reverse()
#combine the arrays        
rows= zip(yls,xls,mineral)  
#name storage locations and filename      
newfilePath1= r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\data_large\2_ProcessedData\6_Further\2002584 R+T+CL_bw_mask_cut.csv'
with open(newfilePath1, "wb") as f:
    writer= csv.writer(f)
    for row in rows:
        writer.writerow(row)
"""
xlsnew= np.asarray(xls)
ylsnew= np.asarray(yls)
mineralnew= np.asarray(mineral)
df= pd.DataFrame(list(zip(yls,xls,mineral)),columns=['Y','X','Mineral'])
df.to_excel(r'R:\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\data_large\4_SpotReferencing\Tables\TR60a_AGmodi_TEST.xlsx')        
"""