import os 
import sys #used to add system path

import datetime

import json

from pyearth.system.define_global_variables import *


from pyhexwatershed.case.pycase import hexwatershed


pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
     iCase_index_in=None, \
         sJob_in=None,\
          iFlag_mode_in=None, \
         aVariable_in = None, \
             aValue_in = None, \
                 sDate_in = None):

    config={}
    # Opening JSON file
    with open(sFilename_configuration_in) as json_file:
        data = json.load(json_file)       
    
    if iFlag_mode_in is not None:
        iFlag_mode = iFlag_mode_in
    else:
        iFlag_mode = 1

    if sDate_in is not None:
        sDate = sDate_in
    else:
        sDate = sDate_default
        pass

    if iCase_index_in is not None:        
        iCase_index = iCase_index_in
    else:       
        #iCase_index = int( config['iCase_index'])
        pass  
    
    oHexwatershed = hexwatershed(data)
    
    return oHexwatershed