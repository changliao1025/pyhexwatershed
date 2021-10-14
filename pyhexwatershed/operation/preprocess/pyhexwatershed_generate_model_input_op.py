import os
from pathlib import Path
from pyearth.system.define_global_variables import *
from pyflowline.operation.intersect_flowline_with_mesh_with_postprocess_op import intersect_flowline_with_mesh_with_postprocess_op
from pyflowline.format.export_vertex_to_shapefile import export_vertex_to_shapefile
from pyflowline.case.pyflowline_read_model_configuration_file import pyflowline_read_model_configuration_file
from pyflowline.case.pycase import flowlinecase

from pyflowline.operation.create_mesh_op import create_mesh_op
from pyflowline.operation.preprocess_flowline_op import preprocess_flowline_op

from pyflowline.format.export_mesh_info_to_json import export_mesh_info_to_json
from pyflowline.format.export_flowline_info_to_json import export_flowline_info_to_json
from pyhexwatershed.algorithm.auxiliary.assign_elevation_to_cell import assign_elevation_to_cell

from pyhexwatershed.algorithm.topology.rebuild_cell_neighbor import rebuild_cell_neighbor
def pyhexwatershed_generate_model_input_op(oHexWatershed):
    iFlag_use_mesh_dem = oHexWatershed.iFlag_use_mesh_dem

    iMesh_type = oHexWatershed.iMesh_type   

    sFilename_pyflowline_config= oHexWatershed.sFilename_model_configuration

    sWorkspace_output_case = oHexWatershed.sWorkspace_output_case

    sWorkspace_pyflowline_output = sWorkspace_output_case + slash + 'pyflowline'

    oPyflowline = pyflowline_read_model_configuration_file(sFilename_pyflowline_config,\
        iFlag_use_mesh_dem_in = iFlag_use_mesh_dem,\
        iFlag_standalone_in=0,\
        iCase_index_in = oHexWatershed.iCase_index ,
        sDate_in = oHexWatershed.sDate,\
        sWorkspace_output_in = sWorkspace_pyflowline_output)
    
    #include all cells
    aCell_original = create_mesh_op(oPyflowline)

    sWorkspace_output_case = oHexWatershed.sWorkspace_output_case
    sFilename_dem = oHexWatershed.sFilename_dem
    sFilename_elevation = oHexWatershed.sFilename_elevation
    #only cell with elevation
    if iFlag_use_mesh_dem == 0:
        aCell_elevation = assign_elevation_to_cell(iMesh_type, aCell_original, sFilename_dem, sFilename_elevation ,sWorkspace_output_case)
    else:
        #dem is within the mesh itself
        aCell_elevation = aCell_original
        pass

    aFlowline = preprocess_flowline_op(oPyflowline)
    #cell using mesh shapefile, same with aCell_elevation
    aCell, aCell_intersect, aFlowline, aCellID_outlet = intersect_flowline_with_mesh_with_postprocess_op(oPyflowline)

    #rebuild neighbor
    aCell = rebuild_cell_neighbor(aCell_elevation, aCell)

   
    #oHexWatershed.lCellID_outlet = lCellID_outlet
    export_flowline_info_to_json(aCell, aCell_intersect, aFlowline, sFilename_json_out=oHexWatershed.sFilename_flowline_info)

    #export mesh info
    export_mesh_info_to_json(aCell, aFlowline, sFilename_json_out=oHexWatershed.sFilename_mesh_info)

    sPath = os.path.dirname(oHexWatershed.sFilename_basin)
    sName  = Path(oHexWatershed.sFilename_basin).stem + '_new.json'
    oHexWatershed.sFilename_basin  =  sPath + slash + sName
    
    sPath = os.path.dirname(oHexWatershed.sFilename_model_configuration)
    sName  = Path(oHexWatershed.sFilename_model_configuration).stem + '_new.json'
    sFilename_configuration  =  sPath + slash + sName

    oHexWatershed.save_as_json(sFilename_configuration)
