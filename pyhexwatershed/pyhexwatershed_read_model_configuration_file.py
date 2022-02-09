import os 
import sys #used to add system path
import datetime
import json

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyflowline.classes.pycase import flowlinecase

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
     iCase_index_in=None, \
         sJob_in=None,\
         aVariable_in = None, \
             aValue_in = None, \
                 sDate_in = None):

    
    # Opening JSON file
    with open(sFilename_configuration_in) as json_file:
        data = json.load(json_file)        
   
    if sDate_in is not None:
        sDate = sDate_in
    else:
        sDate = data["sDate"]
        pass

    if iCase_index_in is not None:        
        iCase_index = iCase_index_in
    else:       
        iCase_index = int( data['iCase_index'])
        pass  

    data["sDate"] = sDate
    data["iCase_index"] = iCase_index
    
    oHexwatershed = hexwatershedcase(data)
    #oHexwatershed.pPyflowline = flowlinecase(data)
    
    return oHexwatershed