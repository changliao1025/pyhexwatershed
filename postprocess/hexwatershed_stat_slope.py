import platform
import os
import sys
from pathlib import Path

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
sExtension_png = '.png'
missing_value = -9999.0

sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string
from toolbox.reader.gdal_read_tiff import gdal_read_tiff


sWorkspace_data = '/Users/liao313/data/hexwatershed'
sWorkspace_out = '/Users/liao313/tmp/03model/hexwatershed'


fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.set_title("Histogram") 
ax.set_xlabel('Slope')
ax.set_ylabel('Frequency')

#read slope
sFilename_in = sWorkspace_data + slash + 'tinpan' + slash +  'raster' + slash +  'slope.tif'
if not os.path.isfile(sFilename_in): 
        print("File is missing")
        exit()

#nrow = 287
nrow = 833
#ncolumn = 317
ncolumn = 939
#ifs = open(sFilename_in, 'rb')
#aSlope = np.fromfile(ifs, '<f4')
dummy = gdal_read_tiff(sFilename_in)
aSlope= dummy[0]
aSlope.shape = (nrow, ncolumn)
#ifs.close()
nan_indices = np.where(aSlope == missing_value)
good_indices = np.where(aSlope != missing_value)
aData = aSlope[good_indices]
print(np.mean(aData))

sns.distplot(aData, kde =False,norm_hist=True, label="Tin Pan" , ax = ax, color='blue')
sns.kdeplot(aData, label="Tin Pan kde", color='red' , bw =1., ax = ax)
#plt.show()
sFilename_png = sWorkspace_data + slash + 'tinpan' + slash +  'raster' + slash +  'slope' + sExtension_png
plt.savefig(sFilename_png, bbox_inches = 'tight')
print(sFilename_png)
#txt file

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.set_title("Histogram") 
ax.set_xlabel('Slope')
ax.set_ylabel('Frequency')
sFilename_in = sWorkspace_data + slash + 'flat_watershed' + slash +  'raster' + slash +  'slope.tif'
if not os.path.isfile(sFilename_in): 
        print("File is missing")
        exit()


#nrow = 287
nrow = 252
#ncolumn = 317
ncolumn = 335
#ifs = open(sFilename_in, 'rb')
#aSlope = np.fromfile(ifs, '<f4')
dummy = gdal_read_tiff(sFilename_in)
aSlope= dummy[0]
aSlope.shape = (nrow, ncolumn)
#ifs.close()
nan_indices = np.where(aSlope == missing_value)
good_indices = np.where(aSlope != missing_value)
aData = aSlope[good_indices]
print(np.mean(aData))
sns.distplot(aData, kde =False,norm_hist=True, label="CBFW" , ax = ax, color='blue')
sns.kdeplot(aData, label="CBFW kde", color='red' , bw =1., ax = ax)
#plt.show()
sFilename_png = sWorkspace_data + slash + 'flat_watershed' + slash +  'raster' + slash +  'slope' + sExtension_png
plt.savefig(sFilename_png, bbox_inches = 'tight')
print(sFilename_png)
