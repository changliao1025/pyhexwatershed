
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
from pyhexwatershed.pyhexwatershed_generate_template_configuration_json_file import pyhexwatershed_generate_template_configuration_json_file

#example
parser = argparse.ArgumentParser()
parser.add_argument("--sMesh_type", help = "sMesh_type",  type = str)
parser.add_argument("--iCase_index", help = "iCase_index",  type = int)
parser.add_argument("--dResolution_meter", help = "dResolution_meter",  type = float)
parser.add_argument("--sDate", help = "sDate",  type = str)
#python notebook.py --sMesh_type hexagon --iCase_index 1 --dResolution_meter 50000 --sDate 20220201
pArgs = parser.parse_args()
if len(sys.argv) == 1:
    sMesh_type = 'mpas'
    iCase_index = 1
    dResolution_meter=5000
    sDate='20220308'
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

sPath = str(Path().resolve())
iFlag_option = 1
iFlag_submit = 1
if iFlag_option ==1:
    sFilename_configuration_in = sPath +  '/tests/configurations/template.json' 
    sWorkspace_data = realpath( sPath +  '/data/susquehanna' )
    oPyhexwatershed = pyhexwatershed_generate_template_configuration_json_file(sFilename_configuration_in, sWorkspace_data, sMesh_type_in=sMesh_type, iCase_index_in = iCase_index, sDate_in = sDate)
    print(oPyhexwatershed.tojson())
else: 
    if iFlag_option == 2:
        #an example configuration file is provided with the repository, but you need to update this file based on your own case study
        #linux
  
        if sMesh_type=='hexagon':
            sFilename_configuration_in = realpath( sPath +  '/../configurations/pyflowline_susquehanna_hexagon.json' )
        else:
            if sMesh_type=='square':
                sFilename_configuration_in = realpath( sPath +  '/../configurations/pyflowline_susquehanna_square.json' )
            else:
                if sMesh_type=='latlon':
                    sFilename_configuration_in = realpath( sPath +  '/../configurations/pyflowline_susquehanna_latlon.json' )
                else:
                    sFilename_configuration_in = realpath( sPath +  '/../configurations/)pyflowline_susquehanna_mpas.json' )
        
      
        print(sFilename_configuration_in)
        oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in)     
        print(oPyhexwatershed.tojson())

if iFlag_submit == 1:
    oPyhexwatershed.creat_case()
else:
    oPyhexwatershed.setup()
    oPyhexwatershed.run_pyflowline()
    oPyhexwatershed.run_hexwatershed()
    oPyhexwatershed.analyze()
    oPyhexwatershed.export()

print('Finished')

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation finished.')
