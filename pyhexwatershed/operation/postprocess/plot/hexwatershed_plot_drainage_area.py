import sys, os, stat
import numpy as np
from pathlib import Path

import subprocess

from pyearth.system.define_global_variables import *
from pyearth.visual.color.create_diverge_rgb_color_hex import create_diverge_rgb_color_hex

from pyearth.visual.barplot.barplot_data_with_reference import barplot_data_with_reference

sRegion = 'columboa_river_basin'

aResolution = ['5km', '10km', '20km', '40km']
nResolution =len(aResolution)



iFlag_outlet =2

if iFlag_outlet==1:
    #outlet
    #5k, case 1 2 3 4
    a1 = np.array([26075.0, 26135, 26253, 26779])
    a1 = a1 * 24973500 # hexagon_area(5000)

    a2 = np.array([6230.0, 6510, 6572, 6621])
    a2 = a2 * 100080000.0 #hexagon_area(10000)

    a3 = np.array([1370, 1736, 1630, 1708])
    a3 = a3 * 399948000.0 # hexagon_area(20000)

    a4 = np.array([354, 461, 285, 467])
    a4 = a4 * 1600000000.0 #hexagon_area(40000)
    #mosart(1/16,1/8,1/4 1/2)
    a5 = np.array([6.436525e+11, 6.543713e+11, 6.880888e+11,6.497589e+11 ] )
    #wbd
    #y1=[6.7E5, 6.7E5]
    y10 = 672786081976
    y_label = r'Drainage area (ratio)'
    sTitle = r'Columbia River Basin'
    sFilename_out= '/people/liao313/data/hexwatershed/columbia_river_basin/figure/crb_drainage_area.png'
else:
    #snake river
    #5k, case 1 2 3 4
    a1 = np.array([11414.0, 11094, 11050, 11047])
    a1 = a1 * 24973500 # hexagon_area(5000)

    a2 = np.array([4079.0, 2788, 2781, 2804])
    a2 = a2 * 100080000.0 #hexagon_area(10000)

    a3 = np.array([640, 705, 639, 646])
    a3 = a3 * 399948000.0 # hexagon_area(20000)

    a4 = np.array([139, 183, 39, 166])
    a4 = a4 * 1600020000.0 #hexagon_area(40000)

    #mosart
    a5 = np.array([255436.673961, 262769.221708, 269008.938857, 262943.274782])*1E6
    #wbd
    y11 = 90764.3
    y12 = 95795.68  #10.639301
    y13 = 92909.9   #10.296657
    y10 = (y11 + y12 + y13 )* 1.0E6
    
    y_label = r'Snake river drainage area (ratio)'
    y_label = r'Drainage area (ratio)'
    sTitle = r'Snake River Basin'
    sFilename_out= '/people/liao313/data/hexwatershed/columbia_river_basin/figure/snake_river_drainage_area.png'

a0 =np.array([y10, y10, y10,y10]) 


iSize_x = 12
iSize_y =  9
iDPI = 150
nData= 6

aLinestyle = [  'solid',  'dotted'  , 'dashed', 'dashdot', 'dashdot', 'solid']

aMarker=  [  '+',  '^'  , 'o', 'p', 'd', '*']
aColor= create_diverge_rgb_color_hex(nData )
aLabel_legend= ['WBD','Nearest','Nearest + stream burning','Zonal mean','Zonal mean + stream burning','DRT']
aHatch = [ '.',   '*', '+', '|', '-', 'o']

sFormat_x = ''

sFormat_y = '%.1f'

#need to transpose
a = np.array([ a1, a2, a3, a4])
a1, a2, a3, a4 = np.transpose(a)
aData= np.array( [a0, a1, a2, a3, a4, a5]) / 1.0E6
aData = aData / (a0/1.0E06)

barplot_data_with_reference(aData, \
             aResolution, \
             aLabel_legend,\
             sFilename_out,\
             dMax_y_in = 2.0,\
             dMin_y_in = 0,\
             sFormat_y_in = sFormat_y,
             sLabel_y_in= y_label,\
             ncolumn_in= 3,\
             aColor_in= aColor,\
             aHatch_in = aHatch,\
             sTitle_in = sTitle)

print('finished')
