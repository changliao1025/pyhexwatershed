import os, sys
#use this function to generate an initial json file for hexwatershed
import json
#once it's generated, you can modify it and use it for different simulations
from pyhexwatershed.case.pycase import hexwatershed
import numpy as np
def pyhexwatershed_generate_case_json_file(sFilename_json):
   
    #sFilename_json = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/compset.json'
    if os.path.exists(sFilename_json): 
        #delete it if it exists
        os.remove(sFilename_json)

 
    #use a dict to initialize the class
    aConfig = {}
    aConfig['iFlag_flowline'] = 1
    aConfig['iFlag_merge_reach'] = 1
    #aConfig['iMesh_type'] = 4 #mpas
    aConfig['iFlag_resample_method'] = 2
    aConfig['lMeshID_outlet'] = -1
    aConfig['sFilename_model_configuration']  = sFilename_json

    aConfig['sWorkspace_data'] = '/people/liao313/data'
    aConfig['sWorkspace_scratch'] = '/compyfs/liao313/'
    aConfig['sWorkspace_project'] = '/pyhexwatershed/susquehanna'
    aConfig['sWorkspace_bin'] = '/people/liao313/bin'
    aConfig['sRegion'] = 'susquehanna'
    aConfig['sModel'] = 'pyhexwatershed'

    aConfig['iCase_index'] = 1
    aConfig['sMesh_type'] = 'mpas'

    aConfig['sDate']= '20210713'

    aConfig['sFilename_mesh'] = 'mpas.shp'
    
    aConfig['sFilename_elevation']  = 'elevation.shp'

    aConfig['sFilename_dem']  = '/qfs/people/liao313/data/hexwatershed/susquehanna/raster/dem/dem_ext.tif'

    aConfig['sFilename_pystream_config'] = '/qfs/people/liao313/workspace/python/pystream/pystream/config/pystream_susquehanna_mpas.xml'

    aConfig['sFilename_spatial_reference'] = '/qfs/people/liao313/data/hexwatershed/susquehanna/vector/hydrology/boundary_proj.shp'
    

    oModel = hexwatershed(aConfig)
    
    oModel.save_as_json(sFilename_json)

    return

