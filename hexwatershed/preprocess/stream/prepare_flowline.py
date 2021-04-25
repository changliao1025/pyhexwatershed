import os, sys
from pyearth.system.define_global_variables import *

from hexwatershed.preprocess.convert_shapefile_to_json import convert_shapefile_to_json
from hexwatershed.preprocess.stream.connect_disconnect_line import connect_disconnect_line

from hexwatershed.preprocess.stream.merge.merge_flowline import merge_flowline
from hexwatershed.preprocess.stream.split.split_flowline import split_flowline, split_flowline2, find_flowline_vertex

from hexwatershed.preprocess.stream.simplification.remove_flowline_loop import remove_flowline_loop
def prepare_flowline(sFilename_shapefile_in,sFilename_mesh_in, sWorkspace_out):
    """
    prepare the flowline using multiple step approach
    """

    #step 1: convert it to json format
    sFilename_json_out = sWorkspace_out + slash + 'flowline1.json'
    #convert_shapefile_to_json( sFilename_shapefile_in, sFilename_json_out)

    #step 3: split into segment
    sFilename_in = sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline3.json'
    split_flowline(sFilename_in,  sFilename_out)

    #connect disconnected vertex
    sFilename_in = sFilename_json_out
    sFilename_out = sWorkspace_out + slash + 'flowline1_connect.json'
    connect_disconnect_line(sFilename_in,  sFilename_out )
    return

    #step 2: merge all as one single feature   
   
    sFilename_in = sFilename_json_out
    sFilename_out = sWorkspace_out + slash + 'flowline2.json'
    merge_flowline(sFilename_in,  sFilename_out )    

    #sFilename_in = sFilename_out
    #sFilename_out = sWorkspace_out + slash + 'flowline3_merge.json'
    #merge_flowline(sFilename_in,  sFilename_out )    

    #step 3: split into segment
    #sFilename_in = sFilename_out
    #sFilename_out = sWorkspace_out + slash + 'flowline3_split.json'
    #split_flowline(sFilename_in,  sFilename_out)   

    #sFilename_in = sFilename_out
    #sFilename_out = sWorkspace_out + slash + 'flowline4_vertex.json'
    #find_flowline_vertex(sFilename_in,  sFilename_out)

    #sFilename_in =  sWorkspace_out + slash + 'flowline3_split.json'
    #sFilename_in2 = sWorkspace_out + slash + 'flowline4_vertex.json'
    #sFilename_out = sWorkspace_out + slash + 'flowline4.json'
    #split_flowline2(sFilename_in, sFilename_in2, sFilename_out)

    #step 4: remove loops
    sFilename_in = sFilename_out    
    sFilename_out = sWorkspace_out + slash + 'flowline5.json'
    remove_flowline_loop(sFilename_in,  sFilename_out)
    

    sFilename_in = sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline6.json'
    merge_flowline(sFilename_in,  sFilename_out )

    #sFilename_in = sFilename_out
    #sFilename_out = sWorkspace_out + slash + 'flowline7.json'
    #split_flowline(sFilename_in,  sFilename_out)
    
    #sFilename_in = sFilename_out
    #sFilename_out = sWorkspace_out + slash + 'flowline7_vertex.json'
    #find_flowline_vertex(sFilename_in,  sFilename_out)

    #sFilename_in = sWorkspace_out + slash + 'flowline7.json'
    #sFilename_in2 = sWorkspace_out + slash + 'flowline7_vertex.json'
    #sFilename_out = sWorkspace_out + slash + 'flowline8.json'
    #split_flowline2(sFilename_in, sFilename_in2, sFilename_out)

    #step 5: remove small headwater segment
    #step 6: intersect with mesh and simplify
    #step 7: rebuild index and order
    #step 8: calculate properties
    print('Finished')

    return


if __name__ == '__main__':
    sFilename_shapefile_in = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/vector/hydrology/crb_flowline.shp'

    sFilename_mesh = 'hexagon.json'
    sWorkspace_out = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin'

    sFilename_mesh_in = os.path.join(sWorkspace_out, sFilename_mesh)

    sFilename_json_out = 'flowline.json'
    sWorkspace_out = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin'
    sFilename_json_out = os.path.join(sWorkspace_out, sFilename_json_out)
    
    prepare_flowline(sFilename_shapefile_in,sFilename_mesh_in, sWorkspace_out)
