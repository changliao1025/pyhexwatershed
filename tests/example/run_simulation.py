
import os, sys
from pathlib import Path
from os.path import realpath
import argparse
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation started.')

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file
from pyhexwatershed.pyhexwatershed_generate_template_configuration_file import pyhexwatershed_generate_template_configuration_file

#example
parser = argparse.ArgumentParser()
parser.add_argument("--sMesh_type", help = "sMesh_type",  type = str)
parser.add_argument("--iCase_index", help = "iCase_index",  type = int)
parser.add_argument("--dResolution_meter", help = "dResolution_meter",  type = float)
parser.add_argument("--sDate", help = "sDate",  type = str)
#python notebook.py --sMesh_type hexagon --iCase_index 1 --dResolution_meter 50000 --sDate 20220201
pArgs = parser.parse_args()

sMesh_type = 'hexagon'
iCase_index = 2
dResolution_meter=5000
sDate='20220404'
sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  str(Path(sWorkspace_data)  /  'output')

if len(sys.argv)> 1:
    sMesh_type = pArgs.sMesh_type
    iCase_index = pArgs.iCase_index
    dResolution_meter=pArgs.dResolution_meter
    sDate = pArgs.sDate
    print(sMesh_type, iCase_index, dResolution_meter, sDate)
else:
    print(len(sys.argv), 'Missing arguaments')
    pass

sPath = str(Path().resolve())

iFlag_submit = 0


#an example configuration file is provided with the repository, but you need to update this file based on your own case study
#linux
if sMesh_type=='hexagon':
    sFilename_configuration_in = realpath( sPath +  '/tests/configurations/pyhexwatershed_susquehanna_hexagon.json' )
else:
    if sMesh_type=='square':
        sFilename_configuration_in = realpath( sPath +  '/tests/configurations/pyhexwatershed_susquehanna_square.json' )
    else:
        if sMesh_type=='latlon':
            sFilename_configuration_in = realpath( sPath +  '/tests/configurations/pyhexwatershed_susquehanna_latlon.json' )
        else:
            sFilename_configuration_in = realpath( sPath +  '/tests/configurations/pyhexwatershed_susquehanna_mpas.json' )
        
      

if os.path.isfile(sFilename_configuration_in):
    print(sFilename_configuration_in)
else:
    print('This shapefile does not exist: ', sFilename_configuration_in )
    exit()
oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
    iCase_index_in=iCase_index, sDate_in= sDate, sMesh_type_in= sMesh_type)     
print(oPyhexwatershed.tojson())

if iFlag_submit == 1:
    oPyhexwatershed.create_hpc_job()
    #oPyhexwatershed.submit_hpc_job()
else:
    if oPyhexwatershed.iFlag_global==1:
        #global simulation
        #we can only suport MPAS/latlon mesh at global scale right now
        pass
    else:
        #regional simulation
        if oPyhexwatershed.iFlag_multiple_outlet ==1:
            pass
        else:
            #single basin example
            if oPyhexwatershed.iMesh_type !=4:
                #non-mpas mesh
                #in this case, we need to use the dem data
                if oPyhexwatershed.iFlag_use_mesh_dem == 0:
                    
                    #use dem
                    oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree=39.4620
                    oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree=-76.0093
                    oPyhexwatershed.setup()
                    oPyhexwatershed.pPyFlowline.dLongitude_left= -79
                    oPyhexwatershed.pPyFlowline.dLongitude_right= -74.5
                    oPyhexwatershed.pPyFlowline.dLatitude_bot= 39.20
                    oPyhexwatershed.pPyFlowline.dLatitude_top= 42.8
                    aCell = oPyhexwatershed.run_pyflowline()
                    aCell_out = oPyhexwatershed.assign_elevation_to_cells()
                    oPyhexwatershed.pPyFlowline.export()
                    oPyhexwatershed.export_config_to_json()
                    
                    oPyhexwatershed.run_hexwatershed()
                    oPyhexwatershed.analyze()
                    oPyhexwatershed.export()
                    pass
                else:
                    #some configuration is wrong
                    print('A dem is needed to retrieve the elevation')
                    pass
                pass
            else:
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

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation finished.')
