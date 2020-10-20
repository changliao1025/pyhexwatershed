import sys, os, stat
import numpy as np
from pathlib import Path
from shutil import copy2

import subprocess

import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from pyes.system.define_global_variables import *
from pyes.visual.color.create_diverge_rgb_color_hex import create_diverge_rgb_color_hex

sRegion = 'columboa_river_basin'

aResolution = ['5k', '10k', '20k', '40k']
nResolution =len(aResolution)

aArea = np.array([ 6.50735e+11, 6.52433e+11,4.42281e+11,6.57428e+11 ,\
    6.23099e+11 , 6.23399e+11, 6.58427e+11, 6.58427e+11,\
        6.38318e+11, 6.57915e+11,  6.43517e+11, 6.37118e+11,\
         5.93606e+11, 6.32007e+11 ,4.20804e+11 , 6.24006e+11,\
             6.43625e+11, 6.543713e+11, 6.88088e+11, 6.497589e+11  ])
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
aLabel_legend= ['NHD','Nearest','Nearest with stream burning','Zonal mean','Zonal mean with stream burning','MOSART']

x = np.arange(1,5,1)

x1=[1,4]
y1=[6.7E5, 6.7E5]
ax.plot( x1, y1, \
                 color = aColor[0], linestyle = aLinestyle[0] ,\
                 marker = aMarker[0] ,\
                 label = aLabel_legend[0])   

for i  in np.arange(1,nData,1):
    dummy_index = np.arange(0, 4, 1) * 4 + i-1
    y = aArea[dummy_index] / 1.0E6
    ax.plot( x, y, \
                 color = aColor[i], linestyle = aLinestyle[i] ,\
                 marker = aMarker[i] ,\
                 label = aLabel_legend[i])

    

ax.axis('on')
#ax.set_xticks(x, aResolution)
sFormat_x = ''
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
ax.set_xlim(0.5, 4.5)
ymin= np.min(aArea)/ 1.0E6
ax.set_ylim(ymin * 0.95, 7.0E5)
ax.set_xticks(x)
ax.set_xticklabels(aResolution,fontsize=13 )
sFormat_y = '%.1e'
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter(  sFormat_y ))  
ax.set_xlabel('Resolution (m)',fontsize=12)
y_label = r'Total drainage area ($km^{2}$)'
ax.set_ylabel(y_label,fontsize=12)
ax.grid(which='major', color='grey', linestyle='--', axis='y')
ax.legend(bbox_to_anchor=(0.5,0.0), loc="lower center", fontsize=12)
#plt.show()
sFilename_out= '/people/liao313/data/hexwatershed/columbia_river_basin/drainage_area.png'
plt.savefig(sFilename_out, bbox_inches='tight')
print('finished')