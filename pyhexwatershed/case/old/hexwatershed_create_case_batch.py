
import sys, os, stat
import numpy as np
from pathlib import Path
from shutil import copy2

import subprocess
import datetime

from pyearth.system.define_global_variables import *

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)


sDate = '20210805'

from pyhexwatershed.case.old.hexwatershed_create_case import hexwatershed_create_case


sRegion = 'columbia_river_basin'
#sRegion = 'susquehanna'


#crb
if sRegion == 'columbia_river_basin':
    aResolution = ['5k', '10k', '20k', '40k']
    aAccumulation_threshold =[1000, 250, 60, 15]
    aMeshID_outlet =[19595, 4848, 1240, 324]
    sFilename_dem='crbdem.tif'
    sMissing_value_dem='-32768'
else:
    #susquehanna
    if sRegion == 'susquehanna':
        aResolution = ['5k', '10k', '20k']
        aAccumulation_threshold =[100, 50, 10]
        aMeshID_outlet =[4664, 1162, 297]
        sFilename_dem='dem1.tif'
        sMissing_value_dem='-9999'
    else:
        #aAccumulation_threshold =[1000, 250, 60, 15]
        pass

nResolution  = len(aResolution)

iCase_index = 1

for i  in np.arange(nResolution):

    #if i !=3 :
    #continue
    iFlag_resample_method = 1

    iCase_index = i* nResolution + 1
    dAccumulation_threshold = aAccumulation_threshold[i]
    sResolution = aResolution[i]

    lMeshID_outlet = aMeshID_outlet[i]
    iFlag_stream_burning_topology = 0
    iFlag_stream_burning = 0
    hexwatershed_create_case(iFlag_resample_method, \
                             iFlag_stream_burning,\
                             iFlag_stream_burning_topology, \
                             iCase_index, \
                             lMeshID_outlet,\
                             dAccumulation_threshold ,  \
                             sDate,\
                             sRegion, \
                             sResolution, \
                             sFilename_dem,\
                             sMissing_value_dem)

    iCase_index = iCase_index + 1
    iFlag_stream_burning_topology = 0
    iFlag_stream_burning = 1
    hexwatershed_create_case(iFlag_resample_method, \
                             iFlag_stream_burning,\
                             iFlag_stream_burning_topology, \
                             iCase_index, \
                             lMeshID_outlet,\
                             dAccumulation_threshold ,  \
                             sDate,\
                             sRegion, \
                             sResolution, \
                             sFilename_dem,\
                             sMissing_value_dem)

    iCase_index = iCase_index + 1
    iFlag_resample_method = 2
    iFlag_stream_burning = 0
    hexwatershed_create_case(iFlag_resample_method, \
                             iFlag_stream_burning,\
                             iFlag_stream_burning_topology, \
                             iCase_index, \
                             lMeshID_outlet,\
                             dAccumulation_threshold ,  \
                             sDate,\
                             sRegion, \
                             sResolution, \
                             sFilename_dem,\
                             sMissing_value_dem)

    iCase_index = iCase_index + 1
    iFlag_resample_method = 2
    iFlag_stream_burning = 1
    iFlag_stream_burning_topology=0

    hexwatershed_create_case(iFlag_resample_method, \
                             iFlag_stream_burning,\
                             iFlag_stream_burning_topology, \
                             iCase_index, \
                             lMeshID_outlet,\
                             dAccumulation_threshold ,  \
                             sDate,\
                             sRegion, \
                             sResolution, \
                             sFilename_dem,\
                             sMissing_value_dem)

pass
