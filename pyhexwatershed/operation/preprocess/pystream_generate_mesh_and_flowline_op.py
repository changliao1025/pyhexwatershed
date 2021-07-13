import os

from pystream.operation.intersect_flowline_with_mesh_with_postprocess_op import intersect_flowline_with_mesh_with_postprocess_op
from pystream.format.export_vertex_to_shapefile import export_vertex_to_shapefile
from pystream.case.pystream_read_model_configuration_file import pystream_read_model_configuration_file
from pystream.case.pycase import streamcase


def pystream_generate_mesh_and_flowline_op(oModel_in):

    sFilename_pystream_config= oModel_in.sFilename_pystream_config

    aParameter = pystream_read_model_configuration_file(sFilename_pystream_config)
    aParameter['sFilename_model_configuration'] = sFilename_pystream_config
    oModel = streamcase(aParameter)


    intersect_flowline_with_mesh_with_postprocess_op(oModel)

