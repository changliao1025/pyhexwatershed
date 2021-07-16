import os

from pystream.operation.intersect_flowline_with_mesh_with_postprocess_op import intersect_flowline_with_mesh_with_postprocess_op
from pystream.format.export_vertex_to_shapefile import export_vertex_to_shapefile
from pystream.case.pystream_read_model_configuration_file import pystream_read_model_configuration_file
from pystream.case.pycase import streamcase

from pystream.operation.create_mesh_op import create_mesh_op
from pystream.operation.preprocess_flowline_op import preprocess_flowline_op

from pystream.format.export_mesh_info_to_json import export_mesh_info_to_json
from pystream.format.export_flowline_info_to_json import export_flowline_info_to_json
from pyhexwatershed.algorithm.auxiliary.assign_elevation_to_cell import assign_elevation_to_cell
def pyhexwatershed_generate_model_input_op(oHexWatershed):

    iMesh_type = oHexWatershed.iMesh_type
    sFilename_elevation = oHexWatershed.sFilename_elevation

    sFilename_pystream_config= oHexWatershed.sFilename_pystream_config

    aParameter = pystream_read_model_configuration_file(sFilename_pystream_config)
    aParameter['sFilename_model_configuration'] = sFilename_pystream_config
    oPystream = streamcase(aParameter)

    aCell = create_mesh_op(oPystream)

    sWorkspace_simulation_case = oHexWatershed.sWorkspace_simulation_case
    sFilename_dem = oHexWatershed.sFilename_dem
    #aCell = assign_elevation_to_cell(iMesh_type, aCell, sFilename_dem, sFilename_elevation ,sWorkspace_simulation_case)

    #export mesh info
    #export_mesh_info_to_json(aCell, sFilename_json_out=oHexWatershed.sFilename_mesh_info)


    #preprocess_flowline_op(oPystream)
    aCell_intersect, aFlowline = intersect_flowline_with_mesh_with_postprocess_op(oPystream)

    export_flowline_info_to_json(aCell_intersect, aFlowline, sFilename_json_out=oHexWatershed.sFilename_flowline_info)
