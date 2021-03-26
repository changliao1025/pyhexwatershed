import sys, os, stat
import numpy as np
from pathlib import Path
from shutil import copy2

import subprocess

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
print(sSystem_paths)
from pyes.system.define_global_variables import *
from pyes.visual.color.create_diverge_rgb_color_hex import create_diverge_rgb_color_hex

from pyes.visual.barplot.barplot_data import barplot_data

sRegion = 'columboa_river_basin'

aResolution = ['5k', '10k', '20k', '40k']
nResolution =len(aResolution)

aArea = np.array([ 6.50735e+11, 6.52433e+11,4.42281e+11,6.57428e+11 ,\
    6.23099e+11 , 6.23399e+11, 6.58427e+11, 6.58427e+11,\
        6.38318e+11, 6.57915e+11,  6.43517e+11, 6.37118e+11,\
         5.93606e+11, 6.32007e+11 ,4.20804e+11 , 6.24006e+11,\
             6.43625e+11, 6.543713e+11, 6.88088e+11, 6.497589e+11  ])



a1 = np.array([11414.0, 11094, 11050, 11047])
a1 = a1 * 24973500 # hexagon_area(5000)

a2 = np.array([4079.0, 2788, 2781, 2804])
a2 = a2 * 100080000.0 #hexagon_area(10000)

a3 = np.array([640, 705, 639, 646])
a3 = a3 * 399948000.0 # hexagon_area(20000)

a4 = np.array([139, 183, 39, 166])
a4 = a4 * 1600020000.0 #hexagon_area(40000)



a5 = np.array([255436.673961, 262769.221708, 269008.938857, 262943.274782])*1E6

aArea = np.array([ a1, a2, a3, a4 , a5 ])
iSize_x = 12
iSize_y =  9
iDPI =150
nData= 6
fig = plt.figure( dpi=iDPI )
fig.set_figwidth( iSize_x )
fig.set_figheight( iSize_y )
ax = fig.add_axes([0.1, 0.5, 0.8, 0.4] )
aLinestyle = [  'solid',  'dotted'  , 'dashed', 'dashdot', 'dashdot', 'solid']
 #np.full(nData, '-')
aMarker=  [  '+',  '^'  , 'o', 'p', 'd', '*']
#np.full(nData, '+')
aColor= create_diverge_rgb_color_hex(nData )
aLabel_legend= ['WBD','Nearest','Nearest with stream burning','Zonal mean','Zonal mean with stream burning','DRT']

x = np.arange(1,5,1)

x1=[1,4]
y11 = 90764.3
y12 = 95795.68  #10.639301
y13 = 92909.9   #10.296657
y10 = (y11 + y12 + y13 ) 

y1=[6.7E5, 6.7E5]
y1=[y10, y10]


aData= []

barplot_data(aData, \
    aResolution, \
        aLabel_legend)


ax.plot( x1, y1, \
                 color = aColor[0], linestyle = aLinestyle[0] ,\
                 marker = aMarker[0] ,\
                 label = aLabel_legend[0])   

for i  in np.arange(1,nData-1,1):
    
    y = aArea[0:4,i-1] / 1.0E6
    ax.plot( x, y, \
                 color = aColor[i], linestyle = aLinestyle[i] ,\
                 marker = aMarker[i] ,\
                 label = aLabel_legend[i])

y = aArea[4,:] / 1.0E6
ax.plot( x, y, \
                 color = aColor[5], linestyle = aLinestyle[5] ,\
                 marker = aMarker[5] ,\
                 label = aLabel_legend[5])
    

ax.axis('on')
#ax.set_xticks(x, aResolution)
sFormat_x = ''
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.set_xlim(0.5, 4.5)
ymin= np.min(aArea)/ 1.0E6
ax.set_ylim(ymin * 0.95, 5.00E5)
ax.set_xticks(x)
ax.set_xticklabels(aResolution,fontsize=13 )
sFormat_y = '%.1e'
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(  sFormat_y ))  
ax.set_xlabel('Resolution (m)',fontsize=12)
y_label = r'Snake river drainage area ($km^{2}$)'
ax.set_ylabel(y_label,fontsize=12)
ax.grid(which='major', color='grey', linestyle='--', axis='y')
ax.legend(bbox_to_anchor=(1.0,1.0), loc="upper right", fontsize=12)
#plt.show()
sFilename_out= '/people/liao313/data/hexwatershed/columbia_river_basin/figure/drainage_area2.png'
plt.savefig(sFilename_out, bbox_inches='tight')
print('finished')