import os

from pyflowline.formats.read_flowline import read_flowline_geojson
from pyflowline.algorithms.split.find_flowline_confluence import find_flowline_confluence
from pyflowline.algorithms.merge.merge_flowline import merge_flowline
from pyflowline.formats.export_flowline import export_flowline_to_geojson
def merge_stream_edge_to_stream_segment(sFilename_stream_edge_geojson_in, 
                                        sFilename_stream_segment_geojson,
                                        pVertex_outlet_in):

    if os.path.exists(sFilename_stream_segment_geojson):
        os.remove(sFilename_stream_segment_geojson)

    aFlowline_edge_basin_conceptual, pSpatialRef_geojson = read_flowline_geojson(sFilename_stream_edge_geojson_in)
    
    #remember there that it is possible that there is only one segment, no confluence
    aVertex, lIndex_outlet, aIndex_headwater,aIndex_middle, aIndex_confluence, aConnectivity, pVertex_outlet_in\
            = find_flowline_confluence(aFlowline_edge_basin_conceptual,  
                                       pVertex_outlet_in)
            #segment based
    aFlowline_basin_conceptual = merge_flowline( aFlowline_edge_basin_conceptual,\
                aVertex, 
                pVertex_outlet_in, 
                aIndex_headwater,
                aIndex_middle, 
                aIndex_confluence  )
    
    #sFilename_stream_segment_geojson = pBasin.sFilename_stream_segment
    
    aStream_segment = list()
    for pFlowline in aFlowline_basin_conceptual:
        aStream_segment.append( pFlowline.iStream_segment  )

    export_flowline_to_geojson(aFlowline_basin_conceptual,
                                sFilename_stream_segment_geojson,
                aAttribute_data=[aStream_segment], 
                aAttribute_field=['iseg'], 
                aAttribute_dtype=['int'])
    return 