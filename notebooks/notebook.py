
from pathlib import Path

import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation started.')

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file
from pyhexwatershed.pyhexwatershed_generate_template_configuration_json_file import pyhexwatershed_generate_template_configuration_json_file

iFlag_option = 1
if iFlag_option ==1:

    sPath = str(Path(__file__).parent.resolve())
    sFilename_configuration_in = sPath +  '/../tests/configurations/template.json' 
    
    oPyhexwatershed = pyhexwatershed_generate_template_configuration_json_file(sFilename_configuration_in)
    print(oPyhexwatershed.tojson())
    #now you can customize the model object
    oPyhexwatershed.iCase_index = 1
    print(oPyhexwatershed.tojson())
else: 
    if iFlag_option == 2:
        #an example configuration file is provided with the repository, but you need to update this file based on your own case study
        #linux
  
        sPath = str(Path(__file__).parent.resolve())
        sFilename_configuration_in = sPath +  '/../tests/configurations/pyhexwatershed_susquehanna_hexagon.json' 
        sFilename_configuration_in = sPath +  '/../tests/configurations/pyhexwatershed_susquehanna_square.json' 
        #sFilename_configuration_in = sPath +  '/../tests/configurations/pyhexwatershed_susquehanna_latlon.json' 
        sFilename_configuration_in = sPath +  '/../tests/configurations/pyhexwatershed_susquehanna_mpas.json' 
        
        #mac
        #sFilename_configuration_in = '/Users/liao313/workspace/python/pyhexwatershed/configurations/pyhexwatershed_susquehanna_hexagon_mac.json'
        print(sFilename_configuration_in)
        oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in)
        #print the case information in details
        print(oPyhexwatershed.tojson())

#pyhexwatershed can process multiple basins within one singel run
exit()
oPyhexwatershed.setup()
oPyhexwatershed.run_pyflowline()
oPyhexwatershed.run()
#oPyhexwatershed.plot_study_area()

oPyhexwatershed.plot(sVariable_in = 'flow_direction')

#aExtent_full = [-78.5,-75.5, 39.2,42.5]
#aExtent_zoom = [-76.0,-76.5, 39.5,40.0] #outlet
#aExtent_zoom = [-76.5,-76.2, 41.6,41.9] #meander
#aExtent_zoom = [-77.3,-76.5, 40.2,41.0] #braided
#aExtent_zoom = [-77.3,-76.5, 40.2,41.0] #confluence
#oPyhexwatershed.plot(sVariable_in = 'final')
#oPyhexwatershed.plot(sVariable_in = 'overlap',aExtent_in=aExtent_full )

#replace conceptual flowline with real flowline length

oPyhexwatershed.export()

print('Finished')

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation finished.')
