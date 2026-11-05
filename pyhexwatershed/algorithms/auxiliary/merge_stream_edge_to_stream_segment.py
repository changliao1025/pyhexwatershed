import os

from pyearthriver.classes.rivergraph import pyrivergraph
from pyflowline.formats.export_flowline import export_flowline_to_geojson
from pyflowline.formats.read_flowline import read_flowline_vector


def merge_stream_edge_to_stream_segment(
    sFilename_stream_edge_geojson_in, sFilename_stream_segment_geojson, pVertex_outlet_in
):

    if os.path.exists(sFilename_stream_segment_geojson):
        os.remove(sFilename_stream_segment_geojson)

    aFlowline_edge_basin_conceptual, pSpatialRef_geojson = read_flowline_vector(
        sFilename_stream_edge_geojson_in
    )

    pRivergraph = pyrivergraph(aFlowline_edge_basin_conceptual, pVertex_outlet_in)
    pRivergraph.define_river_confluence()
    aFlowline_basin_conceptual = pRivergraph.merge_flowline()
    aFlowline_basin_conceptual, aStream_segment = pRivergraph.define_stream_segment()

    export_flowline_to_geojson(
        aFlowline_basin_conceptual,
        sFilename_stream_segment_geojson,
        aAttribute_data=[aStream_segment],
        aAttribute_field=["segment"],
        aAttribute_dtype=["int"],
    )
    return
