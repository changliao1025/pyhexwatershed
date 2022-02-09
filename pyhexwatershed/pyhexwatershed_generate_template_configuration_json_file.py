import os, sys
#use this function to generate an initial json file for hexwatershed
import json
from pathlib import Path
import numpy as np
#once it's generated, you can modify it and use it for different simulations
from pyflowline.classes.pycase import flowlinecase
from pyflowline.classes.basin import pybasin
from pyhexwatershed.classes.pycase import hexwatershedcase

def pyhexwatershed_generate_template_configuration_json_file(sFilename_json):
   
    #sFilename_json = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/compset.json'
    if os.path.exists(sFilename_json): 
        #delete it if it exists
        os.remove(sFilename_json)
    nBasin = 1
 
    #use a dict to initialize the class
    aConfig = {}
    aConfig['iFlag_flowline'] = 1
    aConfig['iFlag_merge_reach'] = 1    
    aConfig['iFlag_resample_method'] = 2       
    aConfig['nOutlet'] = nBasin
    aConfig['dResolution_degree'] = 10000
    aConfig['dResolution_meter'] = 10000
    aConfig['dLongitude_left'] = -180
    aConfig['dLongitude_right'] = 180
    aConfig['dLatitude_bot'] = -90
    aConfig['dLatitude_top'] = 90
    aConfig['sFilename_model_configuration']  = sFilename_json 
    aConfig['sWorkspace_data'] = '/people/liao313/data'
    aConfig['sWorkspace_output'] = "/compyfs/liao313/04model/pyhexwatershed/susquehanna"
    aConfig['sWorkspace_project'] = '/pyhexwatershed/susquehanna'
    aConfig['sWorkspace_bin'] = '/people/liao313/bin'
    aConfig['sRegion'] = 'susquehanna'
    aConfig['sModel'] = 'pyhexwatershed'

    aConfig['iCase_index'] = 1
    aConfig['sMesh_type'] = 'mpas'
  
    aConfig['sFilename_dem']  = '/qfs/people/liao313/data/hexwatershed/susquehanna/raster/dem/dem_ext.tif'

    aConfig['sFilename_pystream_config'] = '/qfs/people/liao313/workspace/python/pyflowline/pyflowline/config/pystream_susquehanna_mpas.xml'

    aConfig['sJob'] = 'pyhexwatershed'
    aConfig['sDate']= '20220110'
    aConfig['sFilename_mesh'] = "/qfs/people/liao313/data/icom/mesh/delaware_lnd_60_30_5_2_v2/lnd_cull_mesh.nc"    
    aConfig['flowline_info'] = 'flowline_info.json'
    aConfig['sFilename_mesh_info'] = 'mesh_info.json'
    aConfig['sFilename_elevation'] = 'elevation.json'
    aConfig['sFilename_dem']  = '/qfs/people/liao313/data/hexwatershed/susquehanna/raster/dem/dem_ext.tif'    
    aConfig['sFilename_spatial_reference'] = '/qfs/people/liao313/data/hexwatershed/susquehanna/vector/hydrology/boundary_proj.shp'
    
    #pyhexwatershed
    oModel = hexwatershedcase(aConfig)
    
    for i in range(nBasin):
        sBasin =  "{:03d}".format(i+1)   
        aConfig_basin = {}
        aConfig['iFlag_dam'] = 1
        aConfig['iFlag_disconnected'] = 1
        aConfig['lBasinID'] = i + 1
        aConfig_basin['dLatitude_outlet_degree'] = -180
        aConfig_basin['dLongitude_outlet_degree'] = 180
        aConfig_basin['dAccumulation_threshold'] = -90
        aConfig_basin['dThreshold_small_river'] = 90
        aConfig_basin['sFilename_dam'] = "/qfs/people/liao313/data/hexwatershed/susquehanna/auxiliary/ICoM_dams.csv"
        aConfig_basin['sFilename_flowline_filter'] = "/qfs/people/liao313/data/hexwatershed/susquehanna/vector/hydrology/streamord7above.shp"
        aConfig_basin['sFilename_flowline_raw'] = "/qfs/people/liao313/data/hexwatershed/susquehanna/vector/hydrology/allflowline.shp"
        aConfig_basin['sFilename_flowline_topo'] = "/qfs/people/liao313/data/hexwatershed/susquehanna/auxiliary/flowline.csv"
        aConfig_basin['sWorkspace_output_basin'] = str(Path(oModel.sWorkspace_output) / sBasin )
        pBasin = pybasin(aConfig_basin)    
        oModel.aBasin.append(pBasin)
        pass

    #export basin config to a file
    sDirname = os.path.dirname(sFilename_json)
    sFilename =  Path(sFilename_json).stem + '_basins.json'
    sFilename_basins = os.path.join(sDirname, sFilename)
    with open(sFilename_basins, 'w', encoding='utf-8') as f:
        sJson = json.dumps([json.loads(ob.tojson()) for ob in oModel.aBasin], indent = 4)        
        f.write(sJson)    
        f.close()

    oModel.sFilename_basins = sFilename_basins
    oModel.export_config_to_json(sFilename_json)

    

    return oModel

