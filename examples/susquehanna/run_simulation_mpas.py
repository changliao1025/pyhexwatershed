
import os, sys
from pathlib import Path
from os.path import realpath

from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file

#===========================
#setup workspace path
#===========================
sPath_parent = str(Path(__file__).parents[2]) # data is located two dir's up
sPath_data = realpath( sPath_parent +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sPath_data)  /  'input')
sWorkspace_output=  str(Path(sPath_data)  /  'output')

#===================================
#you need to update this file based on your own case study
#===================================
sFilename_configuration_in = realpath( sPath_parent +  '/examples/susquehanna/pyhexwatershed_susquehanna_hexagon.json' )
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration file does not exist: ', sFilename_configuration_in )


#===========================
#setup case information
#===========================

iCase_index = 1
dResolution_meter = 5000
sMesh_type = 'mpas'
sDate='20220801'

oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
    iCase_index_in=iCase_index, sDate_in= sDate, sMesh_type_in= sMesh_type)   

if oPyhexwatershed.iFlag_global==1:
    #global simulation
    #we can only suport MPAS/latlon mesh at global scale right now
    pass
else:
    #domain simulation
    if oPyhexwatershed.iFlag_multiple_outlet ==1:
        pass
    else:
        #single basin example       
        #mpas mesh has elevation built-in
        oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree=39.4620
        oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree=-76.0093
        oPyhexwatershed.setup()
        oPyhexwatershed.pPyFlowline.dLongitude_left= -79
        oPyhexwatershed.pPyFlowline.dLongitude_right= -74.5
        oPyhexwatershed.pPyFlowline.dLatitude_bot= 39.20
        oPyhexwatershed.pPyFlowline.dLatitude_top= 42.8
        oPyhexwatershed.run_pyflowline()
        oPyhexwatershed.pPyFlowline.export()
        oPyhexwatershed.export_config_to_json()
        oPyhexwatershed.run_hexwatershed()
        oPyhexwatershed.analyze()
        oPyhexwatershed.export()
        pass
    pass            

print('Finished')

