import os
import sys #used to add system path
import datetime
import json

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyflowline.classes.pycase import flowlinecase

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,
                                                 iCase_index_in=None,
                                                 iFlag_stream_burning_topology_in = None,
                                                 iFlag_elevation_profile_in = None,
                                                 iFlag_use_mesh_dem_in= None,
                                                 dResolution_meter_in = None,
                                                 sDate_in = None,
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

    if iCase_index_in is not None:
        iCase_index = iCase_index_in
    else:
        iCase_index = int( aConfig['iCase_index'])
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

    aConfig["dResolution_meter"] = dResolution_meter
    aConfig["sFilename_model_configuration"] = sFilename_configuration_in


    oPyhexwatershed = hexwatershedcase(aConfig)
    oPyflowline = flowlinecase(aConfig ,  iFlag_standalone_in = 0,
                               sModel_in = 'pyflowline',
                               sWorkspace_output_in = oPyhexwatershed.sWorkspace_output_pyflowline)

    oPyhexwatershed.pPyFlowline = oPyflowline

    return oPyhexwatershed
