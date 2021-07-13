import os, sys
#use this function to generate an initial json file for hexwatershed
import json
#once it's generated, you can modify it and use it for different simulations
from pyhexwatershed.case.pycase import hexwatershed
def pyhexwatershed_generate_case_json_file(sFilename_json):
   
    #sFilename_json = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/compset.json'
    if os.path.exists(sFilename_json): 
        #delete it if it exists
        os.remove(sFilename_json)

 
    #use a dict to initialize the class
    aCompset_para = {}
    aCompset_para['iFlag_flowline'] = 1
    aCompset_para['iFlag_merge_reach'] = 1
    aCompset_para['iFlag_mesh_type'] = 4 #mpas
    aCompset_para['iFlag_resample_method'] = 2
    aCompset_para['lMeshID_outlet'] = -1
    

    oCompset = hexwatershed(aCompset_para)
    
    oCompset.save_as_json(sFilename_json)

    return

