import os, sys
#use this function to generate an initial json file for hexwatershed
import json
#once it's generated, you can modify it and use it for different simulations

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
sPath_pye3sm='/people/liao313/workspace/python/hexwatershed/pyhexwatershed'
sys.path.append(sPath_pye3sm)
from hexwatershed.shared.compset import pycompset
def generate_compset_json_file():
   

 
    #use a dict to initialize the class
    aCompset_para = {}
    aCompset_para['iFlag_flowline'] = 1
    aCompset_para['iFlag_merge_reach'] = 1
    aCompset_para['iFlag_mesh_type'] = 3
    aCompset_para['iFlag_resample_method'] = 2
    aCompset_para['lMeshID_outlet'] = -1
    

    oCompset = pycompset(aCompset_para)
    sFilename_json = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/compset.json'
    oCompset.save_as_json(sFilename_json)

    return
if __name__ == '__main__':
    generate_compset_json_file()
