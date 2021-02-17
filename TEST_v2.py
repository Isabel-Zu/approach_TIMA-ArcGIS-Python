# -*- coding: utf-8 -*-
"""
NOTE: I disabled the plot functions, only the Result-Table is enabled

Created on Wed Jun 24 16:37:20 2020

@author: 20029739
"""

import os
import cv2
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon, MultiPolygon
from descartes import PolygonPatch
import geoplot
import matplotlib
from shapely import speedups
import matplotlib.patches as mpatches
speedups.enabled

#------------------------------------------------------------------------------
## SAMPLE
sample='TR12_AGmodi'

#------------------------------------------------------------------------------
## Functions used in this script
def merge(list1, list2): 
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
    return merged_list 

def get_key(val): 
    for key, value in dictionary.items(): 
         if val == value: 
             return key

#------------------------------------------------------------------------------
## LOAD DATA

## WHOLE THIN-SECTION
# Get all the layers from the .gdb file 
#layers = fiona.listlayers(r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\ArcGIS_server\ThinSections.gdb')
#whole thinsection, POLYGONS
#data_all_poly= gpd.read_file(r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\ArcGIS_server\ThinSections.gdb',layer='TR51_storage')
#whole thinsection,POINTS
data_all_points= pd.read_csv(r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\data_large\4_SpotReferencing\Tables\TR12_AGmodi_TEST.csv',names=['Y','X','Mineral'])
#Change pandas Dataframe to GeoDataFrame, PONTS
data_all_points=gpd.GeoDataFrame(data_all_points, geometry=gpd.points_from_xy(data_all_points.X,data_all_points.Y))

## MEASURED DATA
#measured zircons, polygons
data_measured= gpd.read_file(r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\ArcGIS_server\shapefiles\ProcessThinSections\TR12_AGmodi_poly_conc.shp')
#grain infos of measured zircons
#data_measured_infotab= gpd.read_file(r'R:\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\ArcGIS_server\shapefiles\ProcessThinSections\TR51_poly_conc_tab.dbf')
#multiple buffer around the measured zircons, polygons [20,120 - points=distance]
buffer_20= gpd.read_file(r'R:\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\ArcGIS_server\ProcessThinSections.gdb', layer= 'TR12_AGmodi_poly_conc_rb2')
buffer_120= gpd.read_file(r'R:\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\ArcGIS_server\ProcessThinSections.gdb', layer= 'TR12_AGmodi_poly_conc_rb12')
remove=  gpd.read_file(r'R:\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\ArcGIS_server\ProcessThinSections.gdb', layer= 'TR12_AGmodi_poly_conc_remove')

image= cv2.imread(r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\data_large\3_Images\TIMA_Phases\TR12_AGmodi.png')

ax= data_all_points.plot(color='black', alpha= 0.5)
image1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pixels = np.array(image1)
plt.imshow(pixels[::-1], origin='lower')

buffer_120.plot(ax=ax, color='grey', alpha= 0.2)
buffer_20.plot(ax=ax, color='grey',alpha=0.2)
remove.plot(ax=ax, color='black',alpha=0.2)
data_measured.plot(ax=ax, color='red',alpha=0.4)

#------------------------------------------------------------------------------

## Create color dictionary
dictionary={}
with open (r'R:\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\data_large\1_RawData\TIMA_AppliedGeologymodi_colors.txt') as g:
    next(g)
    for line in g:
        (mineralname, valR, valG, valB)= line.split()
        dictionary[(int(valR), int(valG), int(valB))]= str(mineralname)


#for layer in layers:
    #gdf = gpd.read_file(r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\ArcGIS_server\ThinSections.gdb',layer=layer)
    # Do stuff with the gdf

#print (data_all['Mineral'].unique())

#Build spatial index for the points
data_all_points_sindex= data_all_points.sindex

## PLOTs
#fig= plt.figure(figsize=(12, 10), dpi=80)
#base= data_all_poly.plot(column='Mineral',cmap='tab20',scheme='quantiles')
#buffer_20.plot(ax=base, color='r', alpha=0.5)
#buffer_120.plot(ax=base, color= 'r',alpha=0.3)
#Get points within the buffer Polygons and create a Pie Chart for each buffer,
#that shows the mineral assamblege

## Calculations
#save_results_to = os.path.dirname(r'\\son1.curtin.edu.au\dmp\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\ArcGIS_and_Python\TR60b_AGmodi\bla')

Final_Table_20= pd.DataFrame()
for i in range(len(data_measured)):
    polygon20= buffer_20['geometry'].iloc[i][0]
    #Get the x y value of the points generating that polygon 
    x2,y2= polygon20.exterior.xy
    #Get the bounding box of that polygon
    bounds= [min(x2), min(y2), max(x2), max(y2)]
    #Get the indices of the Points that are likely to be inside the polygon's bounding box
    point_candidate_idx= list(data_all_points_sindex.intersection(bounds))
    point_candidates= data_all_points.loc[point_candidate_idx]
    #Make the precise Point in Polygon query
    final_selection1= point_candidates.loc[point_candidates.within(polygon20)] #!!!!!!!
    #count unique minerals from final selection
    minerals= final_selection1.groupby('Mineral')['Mineral'].count()
    l= minerals.index
    #calculate their amount in perecentage
    s_percent= (100/sum(minerals))*minerals
    #store mineralname and perecentage in a Dataframe and always add to the Dataframe
    #to get a table with columns 'Mineral' 'amount%' 'GrainAge_conc' 'GrainNumber'
    ResultDataFrame= s_percent.rename('Mineral_perc_b1').to_frame()
    ResultDataFrame= ResultDataFrame.join(minerals.rename('Mineral_abs_b1'))
    ResultDataFrame['Conc_Age_b1']= buffer_20['TR60b_p_conc_Concordia'].iloc[i]
    ResultDataFrame['Grain']= buffer_20['TR60b_p_conc_Sample'].iloc[i]
    Final_Table_20= Final_Table_20.append(ResultDataFrame)
    ResultDataFrame= []
    #color_list=[]
    #for j in range(len(minerals)):
        #ccc= get_key(minerals.index[j])
        #cc= [x/255 for x in ccc]
        #color_list.append(cc)
    #ax= minerals.plot.pie(figsize=(10,10), labels=None, fontsize=10, colors=color_list)
    #ax.set_xlabel('Minerals  '+ buffer_20['TR12_p_conc_Sample'].iloc[i] +'  '+ polygon20.centroid.wkt)
    #ax.set_ylabel('')
    #handels=[]
    #for k in range(len(minerals)):
        #label=l[k]+' '+ str(round(s_percent[k],2))+'%'
        #handels_app= mpatches.Patch(color=color_list[k], label=label)
        #handels.append(handels_app)
    #plt.legend(handles=handels)
    point_candidate_idx=[]
    #filename= '\TR12_b1_'+polygon20.centroid.wkt+'.png'
    #plt.savefig(save_results_to + filename, dpi=300)
    #plt.show()
    
    #Check PLot Points and Polygons
    #ax1 = fig.add_subplot(111)
    #ax1.plot(x2,y2,color='red',alpha=0.5)
    #final_selection.plot(ax=ax1, color='black',markersize=2)    
    #plt.fill(x2,y2,'r',alpha=0.5)
    
Final_Table_120= pd.DataFrame()
for i in range(len(data_measured)):
    polygon12= buffer_120['geometry'].iloc[i][0]
    #Get the x y value of the points generating that polygon 
    x12,y12= polygon12.exterior.xy
    #Get the bounding box of that polygon
    bounds= [min(x12), min(y12), max(x12), max(y12)]
    #Get the indices of the Points that are likely to be inside the polygon's bounding box
    point_candidate_idx= list(data_all_points_sindex.intersection(bounds))
    point_candidates= data_all_points.loc[point_candidate_idx]
    #Make the precise Point in Polygon query
    final_selection10= point_candidates.loc[point_candidates.within(polygon12)]
    #count unique minerals from final selection
    minerals= final_selection10.groupby('Mineral')['Mineral'].count()
    l= minerals.index
    #calculate their amount in perecentage
    #s_percent= (100/sum(minerals))*minerals
    #store mineralname and perecentage in a Dataframe and always add to the Dataframe
    #to get a table with columns 'Mineral' 'amount%' 'GrainAge_conc' 'GrainNumber'
    ResultDataFrame= s_percent.rename('Mineral_perc_b10').to_frame()
    ResultDataFrame= ResultDataFrame.join(minerals.rename('Mineral_abs_b10'))
    ResultDataFrame= ResultDataFrame.join(minerals)
    ResultDataFrame['Conc_Age_b10']= buffer_120['TR60b_p_conc_Concordia'].iloc[i]
    ResultDataFrame['Grain_b10']= buffer_120['TR60b_p_conc_Sample'].iloc[i]
    Final_Table_120= Final_Table_120.append(ResultDataFrame)
    ResultDataFrame= []
    #color_list=[]
    #for j in range(len(minerals)):
        #ccc= get_key(minerals.index[j])
        #cc= [x/255 for x in ccc]
        #color_list.append(cc)
    #ax= minerals.plot.pie(figsize=(10,10), labels=None, fontsize=10, colors=color_list)
    #ax.set_xlabel('Minerals  '+ buffer_120['TR12_p_conc_Sample'].iloc[i] +'  '+ polygon12.centroid.wkt)
    #ax.set_ylabel('')
    #handels=[]
    #for k in range(len(minerals)):
        #label=l[k]+' '+ str(round(s_percent[k],2))+'%'
        #handels_app= mpatches.Patch(color=color_list[k], label=label)
        #handels.append(handels_app)
    #plt.legend(handles=handels)
    point_candidate_idx=[]
    #filename= '\TR12_b10_'+polygon12.centroid.wkt+'.png'
    #plt.savefig(save_results_to + filename, dpi=300)
    #plt.show()
    
#------------------------------------------------------------------------------   
## Generate Result Table
result = Final_Table_20.append(Final_Table_120, sort=False)
#get unique minerals
#unique_minerals= result.index.unique()
#groupby unique minerals
#grouped= result.groupby(result.index)
#for i in range(len(unique_minerals)):
    #newdf=grouped.get_group(unique_minerals[i])
    #x_age_20= newdf['Conc_Age_b1']
    #x_age_120= newdf['Conc_Age_b10']
    #y_percent_mineral_20= newdf['Mineral_perc_b1']
    #y_percent_mineral_120= newdf['Mineral_perc_b10']
    #plt.figure()
    #plt.plot(x_age_20,y_percent_mineral_20,'ko', label='buffer1')
    #plt.plot(x_age_120,y_percent_mineral_120,'ro', label='buffer10')
    #plt.legend()
    #plt.title(sample +' '+ unique_minerals[i])
    #plt.xlabel('Age [Ma]')
    #plt.ylabel('amount %')
    #if unique_minerals[i] == 'Hematite/Magnetite':
        #filename='\TR12_Hematite-Magnetite.png'
    #else:
        #filename= '\TR12_'+unique_minerals[i]+'.png'
    #plt.savefig(save_results_to + filename, dpi=300)
    #plt.show()

##SaveResultTable
#result.to_csv(r'R:\ARC-19-New-tools-KIRKLC-SE06887\Isabel Zutterkirch\ArcGIS_and_Python\ResultTR60b_AGmodi.csv')




