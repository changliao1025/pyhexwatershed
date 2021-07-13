from pyhexwatershed.case.pycase import hexwatershed

from pyhexwatershed.case.pyhexwatershed_generate_case_json_file import pyhexwatershed_generate_case_json_file

from pyhexwatershed.case.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file
#aParameter=dict()

#aParameter[]=
sFilename_configuration = '/qfs/people/liao313/workspace/python/pyhexwatershed/pyhexwatershed/config/susquehanna.json'


pyhexwatershed_generate_case_json_file(sFilename_configuration)


oModel = pyhexwatershed_read_model_configuration_file(sFilename_configuration)



