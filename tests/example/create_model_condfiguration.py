
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
from pyhexwatershed.pyhexwatershed_generate_template_configuration_file import pyhexwatershed_generate_template_configuration_file

#example
parser = argparse.ArgumentParser()
parser.add_argument("--sMesh_type", help = "sMesh_type",  type = str)
parser.add_argument("--iCase_index", help = "iCase_index",  type = int)
parser.add_argument("--dResolution_meter", help = "dResolution_meter",  type = float)
parser.add_argument("--sDate", help = "sDate",  type = str)
#python notebook.py --sMesh_type hexagon --iCase_index 1 --dResolution_meter 50000 --sDate 20220201
pArgs = parser.parse_args()
if len(sys.argv) == 1:
    sMesh_type = 'latlon'
    iCase_index = 5
    dResolution_meter=10000
    sDate='20220404'
else:
    if len(sys.argv)> 1:
        sMesh_type = pArgs.sMesh_type
        iCase_index = pArgs.iCase_index
        dResolution_meter=pArgs.dResolution_meter
        sDate = pArgs.sDate
        print(sMesh_type, iCase_index, dResolution_meter, sDate)
    else:
        print(len(sys.argv), 'Missing arguaments')
        pass


sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/susquehanna' )
sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')
sWorkspace_output=  str(Path(sWorkspace_data)  /  'output')
sWorkspace_output = '/compyfs/liao313/04model/pyhexwatershed/susquehanna'
sWorkspace_bin = realpath( sPath +  '/bin' )

sFilename_configuration_in = sPath +  '/tests/configurations/pyhexwatershed_susquehanna_latlon.json' 
sWorkspace_data = realpath( sPath +  '/data/susquehanna' )
oPyhexwatershed = pyhexwatershed_generate_template_configuration_file(sFilename_configuration_in,sWorkspace_bin, sWorkspace_input, sWorkspace_output, iFlag_use_mesh_dem_in = 0, sMesh_type_in=sMesh_type, iCase_index_in = iCase_index, sDate_in = sDate)
print(oPyhexwatershed.tojson())


logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation finished.')
