import os, sys
#use this function to generate an initial json file for hexwatershed
import json
from pathlib import Path
import numpy as np
#once it's generated, you can modify it and use it for different simulations
from pyflowline.classes.pycase import flowlinecase
from pyflowline.classes.basin import pybasin
from pyflowline.pyflowline_generate_template_configuration_file import pyflowline_generate_basin_template_configuration_file
from pyhexwatershed.classes.pycase import hexwatershedcase

def pyhexwatershed_generate_template_configuration_file(sFilename_json, sWorkspace_bin, sWorkspace_input, sWorkspace_output, iFlag_use_mesh_dem_in=None,  iFlag_use_shapefile_extent_in=None, iCase_index_in=None, dResolution_degree_in = None,dResolution_meter_in = None,sDate_in = None,sMesh_type_in = None,  sModel_in = None,sWorkspace_output_in = None,):
    """generate hexwatershed config file

    Args:
        sFilename_json (_type_): _description_
        sWorkspace_data_in (_type_): _description_
        sWorkspace_bin_in (_type_): _description_. Defaults to None.
        iFlag_use_mesh_dem_in (_type_, optional): _description_. Defaults to None.
        iFlag_use_shapefile_extent_in (_type_, optional): _description_. Defaults to None.
        iCase_index_in (_type_, optional): _description_. Defaults to None.
        dResolution_degree_in (_type_, optional): _description_. Defaults to None.
        dResolution_meter_in (_type_, optional): _description_. Defaults to None.
        sDate_in (_type_, optional): _description_. Defaults to None.
        sMesh_type_in (_type_, optional): _description_. Defaults to None.
        sModel_in (_type_, optional): _description_. Defaults to None.
        sWorkspace_output_in (_type_, optional): _description_. Defaults to None.
        

    Returns:
        _type_: _description_
    """
    if os.path.exists(sFilename_json):         
        os.remove(sFilename_json)

    if iCase_index_in is not None:        
        iCase_index = iCase_index_in
    else:       
        iCase_index = 1
    if iFlag_use_mesh_dem_in is not None:        
        iFlag_use_mesh_dem = iFlag_use_mesh_dem_in
    else:       
        iFlag_use_mesh_dem = 0
    if iFlag_use_shapefile_extent_in is not None:        
        iFlag_use_shapefile_extent = iFlag_use_shapefile_extent_in
    else:       
        iFlag_use_shapefile_extent = 0



    if sMesh_type_in is not None:
        sMesh_type = sMesh_type_in
    else:
        sMesh_type = 'hexagon'
        pass
    if sDate_in is not None:
        sDate = sDate_in
    else:
        sDate = '20220202'
        pass    

    if dResolution_meter_in is not None:
        dResolution_meter = dResolution_meter_in
    else:
        dResolution_meter = 10000
        pass  
    
    nBasin =1
    
 
    #use a dict to initialize the class
    aConfig = {}
    aConfig['iFlag_use_shapefile_extent'] = iFlag_use_shapefile_extent 
    aConfig['iFlag_flowline'] = 1
    aConfig['iFlag_merge_reach'] = 1    
    
    aConfig['iFlag_use_mesh_dem'] = iFlag_use_mesh_dem
    aConfig['iFlag_save_mesh'] = 1

    aConfig['iFlag_simplification']=1
    aConfig['iFlag_create_mesh']=1
    aConfig['iFlag_intersect']=1
    aConfig['iFlag_resample_method']=2
    aConfig['iFlag_global']=0
    aConfig['iFlag_multiple_outlet']=0
    aConfig['iFlag_elevation_profile']=0
    aConfig['iFlag_rotation']=0
    aConfig['iFlag_stream_burning_topology']=1
    aConfig['iFlag_save_elevation']=1

    aConfig['nOutlet'] = nBasin
    aConfig['dResolution_degree'] = 0.5
    aConfig['dResolution_meter'] =dResolution_meter
    aConfig['dLongitude_left'] = -180
    aConfig['dLongitude_right'] = 180
    aConfig['dLatitude_bot'] = -90
    aConfig['dLatitude_top'] = 90

    aConfig['sFilename_model_configuration']  = sFilename_json 
    aConfig['sWorkspace_input'] = sWorkspace_input
    aConfig['sWorkspace_output'] = sWorkspace_output
  
    aConfig['dAccumulation_threshold'] = 100000
   
    aConfig['sRegion'] = 'susquehanna'
    aConfig['sModel'] = 'pyhexwatershed'

    aConfig['iCase_index'] = iCase_index
    aConfig['sMesh_type'] = sMesh_type
  
    aConfig['sFilename_dem']  = str(Path(sWorkspace_input)  /  'dem_ext.tif')
    aConfig['sFilename_hexwatershed'] = 'hexwatershed'

    aConfig['sFilename_pyflowline_config'] = sFilename_json

    aConfig['sJob'] = 'pyhexwatershed'
    aConfig['sDate']= sDate
    aConfig['sFilename_mesh_netcdf'] = str(Path(sWorkspace_input)  /  'lnd_cull_mesh.nc')
    aConfig['flowline_info'] = 'flowline_info.json'
    aConfig['sFilename_mesh_info'] = 'mesh_info.json'
    aConfig['sFilename_elevation'] = 'elevation.json'
    aConfig['sWorkspace_bin'] = sWorkspace_bin

   
    aConfig['sFilename_spatial_reference'] = str(Path(sWorkspace_input)  /  'boundary_proj.shp')
    
    #pyhexwatershed
    oPyhexwatershed = hexwatershedcase(aConfig)

    oPyflowline = flowlinecase(aConfig ,  iFlag_standalone_in = 0,\
             sModel_in = 'pyflowline',\
                     sWorkspace_output_in = oPyhexwatershed.sWorkspace_output_pyflowline)

    sDirname = os.path.dirname(sFilename_json)
    sFilename =  Path(sFilename_json).stem + '_basins.json'
    sFilename_basins_json = os.path.join(sDirname, sFilename)
  

    aBasin = pyflowline_generate_basin_template_configuration_file(sFilename_basins_json, nBasin, sWorkspace_input , oPyflowline.sWorkspace_output)
    oPyflowline.sFilename_basins = sFilename_basins_json
    oPyflowline.aBasin = aBasin
    oPyhexwatershed.pPyFlowline = oPyflowline

    oPyhexwatershed.sFilename_basins = sFilename_basins_json    

    
    oPyhexwatershed.export_config_to_json(sFilename_json)

    

    return oPyhexwatershed

