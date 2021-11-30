from pyhexwatershed.operation.preprocess.pyhexwatershed_generate_model_input_op import pyhexwatershed_generate_model_input_op
from pyhexwatershed.case.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file


#sFilename_configuration_in = '/qfs/people/liao313/workspace/python/pyhexwatershed/pyhexwatershed/config/hexwatershed_susquehanna_mpas.json'

sFilename_configuration_in = '/qfs/people/liao313/workspace/python/pyhexwatershed/pyhexwatershed/config/hexwatershed_icom_mpas.json'

#sFilename_configuration_in = '/qfs/people/liao313/workspace/python/pyhexwatershed/pyhexwatershed/config/hexwatershed_global_mpas.json'
oModel = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in)

pyhexwatershed_generate_model_input_op(oModel)

print("Finished")

