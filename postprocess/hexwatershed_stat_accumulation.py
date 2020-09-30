
import os
import sys


from shutil import copyfile
import numpy as np
from numpy  import array



import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

import seaborn as sns

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from eslib.system.define_global_variables import *

sRegion = 'tinpan'
sModel= 'hexwatershed'



sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from eslib.toolbox.reader.text_reader_string import text_reader_string

sWorkspace_out = sWorkspace_models + slash + sModel + slash + sRegion


fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.set_title("") 
ax.set_xlabel('Flow Accumulation')
ax.set_ylabel('Frequency')
ax.set_xlim(0, 25)

#raster 
sFilename_in = '/people/liao313/data/hexwatershed/tinpan/raster/hydrology/accumulation'
if not os.path.isfile(sFilename_in): 
    print("File is missing")
    exit()

nrow = 287
ncolumn = 317
ifs = open(sFilename_in, 'rb')
aAccumulation_old = np.fromfile(ifs, '<f4')
aAccumulation_old.shape = (nrow, ncolumn)
ifs.close()
nan_indices = np.where(aAccumulation_old == missing_value)
good_indices = np.where(aAccumulation_old != missing_value)

aAccumulation_old = aAccumulation_old[aAccumulation_old >= 0.0] 
aAccumulation_old = aAccumulation_old[aAccumulation_old < 40.0 ]

#plt.hist(aAccumulation_old, bins = aBin, color='red',alpha = 0.5) 
#plt.title("histogram") 

#sns.distplot(aAccumulation_old, kde =False,norm_hist=True, label="Square grid" , ax = ax, color='blue')
#sns.kdeplot(aAccumulation_old, label="Square grid kde", color='red' , bw =1, ax = ax, clip= (0.0, 45.0))
#plt.show()
#txt file
sFilename_in = '/people/liao313/data/hexwatershed/tinpan/raster/hydrology/flow_accumulation.csv'

#read the attribute table

if not os.path.isfile(sFilename_in): 
        print("File is missing")
        exit()
aData = text_reader_string(sFilename_in, iSkipline_in =1, cDelimiter_in=',', iFlag_remove_quota =1)
#print(aData)

aAccumulation = (  aData[:, 1])
aAccumulation.shape = len(aAccumulation)
aAccumulation = [float(dummy) for dummy in aAccumulation]
aAccumulation = np.array(aAccumulation)
aAccumulation_new = aAccumulation[aAccumulation >= 0.0 ]
aAccumulation_new = aAccumulation_new[aAccumulation_new < 40.0 ]


aBin = np.arange(15, dtype =int)

#plt.hist(aAccumulation_new, bins = aBin) 

#x = np.random.normal(size=100)
#ax = sns.distplot(x)

bin_list = np.arange(0, 45, 1)
plt.hist([aAccumulation_old, aAccumulation_new], label=[ 'SGSD Accumulation', "HGSD Accumulation" ], bins= bin_list )# , color=['red','blue'])
#sns.kdeplot(aAccumulation_new,  label="Hexagon grid kde", color='yellow', bw =1, clip= (0.0, 45.0) )
ax.legend()

#plt.show()
sFilename_out = '/people/liao313/data/hexwatershed/tinpan/raster/hydrology/flow_accumulation_histogram.png'

plt.savefig(sFilename_out, bbox_inches='tight')

#difference
#sFilename_in =sWorkspace_out + slash + 'accu30diff2.dat'
#if not os.path.isfile(sFilename_in): 
#        print("File is missing")
#        exit()
#
#nrow = 287
#ncolumn = 317
#ifs = open(sFilename_in, 'rb')
#aAccumulation_diff = np.fromfile(ifs, '<f4')
#aAccumulation_diff.shape = (nrow, ncolumn)
#ifs.close()
#nan_indices = np.where(aAccumulation_diff == missing_value)
#good_indices = np.where(aAccumulation_diff != missing_value)
#
#aAccumulation_diff = aAccumulation_diff[good_indices] 
#aAccumulation_diff = aAccumulation_diff[aAccumulation_diff < 40.0 ]
#aAccumulation_diff = aAccumulation_diff[aAccumulation_diff > -40.0 ]
##aAccumulation_diff = aAccumulation_diff[aAccumulation_diff != 0.0 ]
#
#aBin = np.arange(80, dtype =int) -40
##plt.hist(aAccumulation_diff, bins = aBin, color='red',alpha = 0.5) 
##plt.title("histogram") 
##plt.show()
#
#fig, ax = plt.subplots(1, 1, figsize=(8, 6))
#ax.set_title("Histogram") 
#ax.set_xlabel('Accumulation difference')
#ax.set_ylabel('Frequency')
#sns.distplot(aAccumulation_diff,kde =False,norm_hist=True, ax = ax, color='blue')
#sns.kdeplot(aAccumulation_diff, label='kde', color='red', bw=1)
#ax.legend()
#
#plt.show()