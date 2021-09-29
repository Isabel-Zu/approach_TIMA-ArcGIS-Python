# Python 3.7
# -*- coding: utf-8 -*-
"""
This script saves x|y positions of vertices, which build up contours of each object 
within an image, into csv files. NOTE: Image background must be 'white-ish'.

WORKFLOW:
    1. Load image
    2. Mask the image objects, draw contours of those objects
    3. Creates a box, based on the coutour-xy-coordinates around the objects
    4. Store the x- and y-coordinates in csv-files

USER INPUT:
    Image - Location\filename.png (line 56)
    Storage - filename.csv (line 107 and 111)
    
Created: 02/07/2020
Last modified: 08/09/2021
Author: Isabel Zutterkirch
"""

#------------------------------------------------------------------------------
## USED MODULES

import cv2
import matplotlib.pyplot as plt
import csv

#------------------------------------------------------------------------------
## USED FUNCTIONS

def sort_contours(cnts, method="top-to-bottom"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if sorting in reversed order is needed
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box is needed
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts)

#------------------------------------------------------------------------------       
##INPUT

# image
image= cv2.imread(r'C:\foldername\imagename.png')

#------------------------------------------------------------------------------
## PROCESSING

# transfer image into a binary image
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# plot image just as a check 
plt.imshow(grayImage)
# mask the objects in the image based on the white background
lower = 139
upper = 255
shapeMask = cv2.inRange(grayImage, lower, upper)
# check if the objects are masked, if not change the 'lower' and 'upper' values
plt.imshow(shapeMask)
# find the contours in the masked image
cnts,hierarchy = cv2.findContours(shapeMask.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)[-2:]
# sort the contours using the function 'sort_contours'
sorted_cnts = sort_contours(cnts)

# iterate over the number of contours if the area is significant enough to capture
# an 'real' object and not just image noise -therefore, check the image, which is
# showing now the contours. Another iteration stores the x|y coordinates of vertices,
# which build up the contour.
# create empty lists for storage
Xcoo=[]
Ycoo=[]
Area=[]
# iteration over object's contour
for n in range(len(sorted_cnts)):
    cnts_area=cv2.contourArea(sorted_cnts[n])
    if cnts_area>50:
        Area.append(cnts_area)
        #create empty lists for storage
        X=[]
        Y=[]
        #iterate over one contour to get its x,y values
        for i in sorted_cnts[n]:
            x= i[0][0]
            y= i[0][1]           
            X.append(x)
            Y.append(y)
        Xcoo.append(X)
        Ycoo.append(Y)
        plt.plot(X,Y,linewidth=1.5)
    else:
        pass

#------------------------------------------------------------------------------
## OUTPUT

# save the x,y values in csv files 
with open("SampleID_Xcoordinates.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(Xcoo)
        
with open("SampleID_Ycoordinates.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(Ycoo)
   
