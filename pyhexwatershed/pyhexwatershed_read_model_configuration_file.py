import os
import sys #used to add system path
import datetime
import json
from pathlib import Path
from pyhexwatershed.classes.pycase import hexwatershedcase
from pyflowline.classes.pycase import flowlinecase
from pyflowline.classes.basin import pybasin
pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,
                                                 iCase_index_in=None,
                                                 iFlag_stream_burning_topology_in = None,
                                                 iFlag_elevation_profile_in = None,
                                                 iFlag_use_mesh_dem_in= None,
                                                 iResolution_index_in = None,
                                                 dResolution_meter_in = None,
                                                 sDate_in = None,
                                                 sDggrid_type_in = None,
                                                 sMesh_type_in=None):


    # Opening JSON file
    with open(sFilename_configuration_in) as json_file:
        aConfig = json.load(json_file)

    if sDate_in is not None:
        sDate = sDate_in
    else:
        sDate = aConfig["sDate"]
        pass

    if sMesh_type_in is not None:
        sMesh_type = sMesh_type_in
    else:
        sMesh_type = aConfig["sMesh_type"]
        pass

    if sDggrid_type_in is not None:
        sDggrid_type = sDggrid_type_in
    else:
        if "sDggrid_type" in aConfig:            
            sDggrid_type = aConfig["sDggrid_type"]
        else:
            sDggrid_type = 'ISEA3H'
            
    if iCase_index_in is not None:
        iCase_index = iCase_index_in
    else:
        iCase_index = int( aConfig['iCase_index'])
        pass

    if iResolution_index_in is not None:    
        iResolution_index = iResolution_index_in
    else:
        if "iResolution_index" in aConfig:            
            iResolution_index =  int( aConfig['iResolution_index'])
        else:
            iResolution_index = 10
      
        pass

    if iFlag_stream_burning_topology_in is not None:
        iFlag_stream_burning_topology = iFlag_stream_burning_topology_in
    else:
        iFlag_stream_burning_topology = int( aConfig['iFlag_stream_burning_topology'])
        pass

    if iFlag_elevation_profile_in is not None:
        iFlag_elevation_profile = iFlag_elevation_profile_in
    else:
        iFlag_elevation_profile = int( aConfig['iFlag_elevation_profile'])
        pass

    if iFlag_use_mesh_dem_in is not None:
        iFlag_use_mesh_dem = iFlag_use_mesh_dem_in
    else:
        iFlag_use_mesh_dem = int( aConfig['iFlag_use_mesh_dem'])
        pass


    if dResolution_meter_in is not None:
        dResolution_meter = dResolution_meter_in
    else:
        dResolution_meter = float( aConfig['dResolution_meter'])
        pass

    aConfig["sDate"] = sDate
    aConfig["sMesh_type"] = sMesh_type
    aConfig["iCase_index"] = iCase_index
    aConfig["iFlag_stream_burning_topology"] = iFlag_stream_burning_topology
    aConfig["iFlag_elevation_profile"] = iFlag_elevation_profile
    aConfig["iFlag_use_mesh_dem"] = iFlag_use_mesh_dem
    aConfig["iResolution_index"] = iResolution_index
    aConfig["dResolution_meter"] = dResolution_meter
    aConfig["sFilename_model_configuration"] = sFilename_configuration_in
    aConfig["sDggrid_type"] = sDggrid_type

    oPyhexwatershed = None
    oPyflowline = None
    oPyhexwatershed = hexwatershedcase(aConfig)
    oPyflowline = flowlinecase(aConfig ,  iFlag_standalone_in = 0,
                               sModel_in = 'pyflowline',
                               sWorkspace_output_in = oPyhexwatershed.sWorkspace_output_pyflowline)
    
    oPyhexwatershed.dResolution_meter = oPyflowline.dResolution_meter

    oPyhexwatershed.pPyFlowline = oPyflowline

    oPyhexwatershed.aBasin.clear()

    #set up the basin object
    with open(oPyhexwatershed.sFilename_basins) as json_file:
        dummy_data = json.load(json_file)
        for i in range(oPyhexwatershed.nOutlet):
            sBasin =  "{:08d}".format(i+1)
            dummy_basin = dummy_data[i]
            dummy_basin['sWorkspace_output_basin'] = str(Path(oPyhexwatershed.sWorkspace_output_hexwatershed) / sBasin )
            pBasin = pybasin(dummy_basin)
            oPyhexwatershed.aBasin.append(pBasin)

    return oPyhexwatershed
