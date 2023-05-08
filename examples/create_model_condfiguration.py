
import sys
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
from pyhexwatershed.pyhexwatershed_create_template_configuration_file import pyhexwatershed_create_template_configuration_file


sMesh_type = 'latlon'
iCase_index = 5
dResolution_meter=10000
sDate='20220404'



sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  str(Path(sWorkspace_data)  /  'output')
sWorkspace_output = '/compyfs/liao313/04model/pyhexwatershed/susquehanna'


sFilename_configuration_in = sPath +  '/tests/configurations/pyhexwatershed_susquehanna_latlon.json' 
sWorkspace_data = realpath( sPath +  '/data/susquehanna' )
oPyhexwatershed = pyhexwatershed_create_template_configuration_file(sFilename_configuration_in, sWorkspace_input, sWorkspace_output, iFlag_use_mesh_dem_in = 0, sMesh_type_in=sMesh_type, iCase_index_in = iCase_index, sDate_in = sDate)
print(oPyhexwatershed.tojson())


logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation finished.')
