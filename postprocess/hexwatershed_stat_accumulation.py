import platform
import os
import sys
from pathlib import Path
import scipy.ndimage as ndimage
import numpy as np
from numpy  import array
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from shutil import copyfile
import seaborn as sns
sPlatform_os = platform.system()
sRegion = 'tinpan'

if sPlatform_os == 'Windows':  #windows
    slash = '\\'
    sWorkspace_code = 'C:' + slash + 'workspace'
    sWorkspace_scratch = 'D:'
    sFilename_config = sRegion + '_windows.txt'
else:  #linux or unix
    slash = '/'
    home = str(Path.home())
    sWorkspace_code = home + slash + 'workspace'
    if (sPlatform_os == 'Linux'):
        sWorkspace_scratch = slash + 'pic' + slash + 'scratch' + slash + 'liao313'
        sFilename_config = sRegion + '_linux.txt'
    else:
        if (sPlatform_os == 'Darwin'):
            sWorkspace_scratch = slash + 'Volumes' + slash + 'mac'
            sFilename_config = sRegion + '_mac.txt'
        else:
            exit
sExtension_envi = '.dat'
sExtension_header = '.hdr'
sExtension_txt = '.txt'
missing_value = -9999.0

sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

sWorkspace_out = '/Users/liao313/tmp/03model/hexwatershed'


fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.set_title("Histogram") 
ax.set_xlabel('Accumulation')
ax.set_ylabel('Frequency')

#raster 
sFilename_in =sWorkspace_out + slash + 'accumulation.dat'
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

aAccumulation_old = aAccumulation_old[aAccumulation_old > 0.0] 
aAccumulation_old = aAccumulation_old[aAccumulation_old < 40.0 ]

#plt.hist(aAccumulation_old, bins = aBin, color='red',alpha = 0.5) 
#plt.title("histogram") 

sns.distplot(aAccumulation_old, kde =False,norm_hist=True, label="Square grid" , ax = ax, color='blue')
sns.kdeplot(aAccumulation_old, label="Square grid kde", color='red' , bw =1., ax = ax)
#plt.show()
#txt file
sFilename_in = sWorkspace_out + slash + 'accumulation30.txt'

#read the attribute table

if not os.path.isfile(sFilename_in): 
        print("File is missing")
        exit()
aData = text_reader_string(sFilename_in, skipline_in =1, delimiter_in=',', remove_quota =1)
#print(aData)

aAccumulation = (  aData[:, 1])
aAccumulation.shape = len(aAccumulation)
aAccumulation = [float(dummy) for dummy in aAccumulation]
aAccumulation = np.array(aAccumulation)
aAccumulation_new = aAccumulation[aAccumulation > 0.0 ]
aAccumulation_new = aAccumulation_new[aAccumulation_new < 40.0 ]


aBin = np.arange(15, dtype =int)

#plt.hist(aAccumulation_new, bins = aBin) 

#x = np.random.normal(size=100)
#ax = sns.distplot(x)

sns.distplot(aAccumulation_new, label="Hexagon grid", kde =False,norm_hist=True, hist_kws=dict(alpha=0.5),ax = ax, color='green')
sns.kdeplot(aAccumulation_new,  label="Hexagon grid kde", color='yellow', bw =1.)
ax.legend()

plt.show()

#difference
sFilename_in =sWorkspace_out + slash + 'accu30diff2.dat'
if not os.path.isfile(sFilename_in): 
        print("File is missing")
        exit()

nrow = 287
ncolumn = 317
ifs = open(sFilename_in, 'rb')
aAccumulation_diff = np.fromfile(ifs, '<f4')
aAccumulation_diff.shape = (nrow, ncolumn)
ifs.close()
nan_indices = np.where(aAccumulation_diff == missing_value)
good_indices = np.where(aAccumulation_diff != missing_value)

aAccumulation_diff = aAccumulation_diff[good_indices] 
aAccumulation_diff = aAccumulation_diff[aAccumulation_diff < 40.0 ]
aAccumulation_diff = aAccumulation_diff[aAccumulation_diff > -40.0 ]
#aAccumulation_diff = aAccumulation_diff[aAccumulation_diff != 0.0 ]

aBin = np.arange(80, dtype =int) -40
#plt.hist(aAccumulation_diff, bins = aBin, color='red',alpha = 0.5) 
#plt.title("histogram") 
#plt.show()

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.set_title("Histogram") 
ax.set_xlabel('Accumulation difference')
ax.set_ylabel('Frequency')
sns.distplot(aAccumulation_diff,kde =False,norm_hist=True, ax = ax, color='blue')
sns.kdeplot(aAccumulation_diff, label='kde', color='red', bw=1)
ax.legend()

plt.show()