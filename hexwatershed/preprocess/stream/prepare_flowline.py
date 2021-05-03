import os, sys
from pyearth.system.define_global_variables import *

from hexwatershed.preprocess.convert_shapefile_to_json import convert_shapefile_to_json
from hexwatershed.preprocess.stream.connect_disconnect_line import connect_disconnect_line
from hexwatershed.preprocess.stream.correct_flowline_direction import correct_flowline_direction

from hexwatershed.preprocess.stream.merge.merge_flowline import merge_flowline
from hexwatershed.preprocess.stream.merge.merge_flowline2 import merge_flowline2

from hexwatershed.preprocess.stream.split.split_flowline import split_flowline
from hexwatershed.preprocess.stream.split.split_flowline2 import split_flowline2
from hexwatershed.preprocess.stream.split.split_flowline3 import split_flowline3

from hexwatershed.preprocess.stream.split.find_flowline_vertex import find_flowline_vertex
from hexwatershed.preprocess.stream.split.find_flowline_vertex2 import find_flowline_vertex2

from hexwatershed.preprocess.stream.simplification.remove_flowline_loop import remove_flowline_loop
from hexwatershed.preprocess.stream.simplification.remove_flowline_loop2 import remove_flowline_loop2
from hexwatershed.preprocess.stream.simplification.remove_flowline_loop3 import remove_flowline_loop3

from hexwatershed.preprocess.stream.simplification.remove_small_river import remove_small_river

from hexwatershed.preprocess.stream.define_stream_order import define_stream_order
from hexwatershed.preprocess.mesh.intersect_flowline_with_mesh import intersect_flowline_with_mesh
def prepare_flowline(sFilename_shapefile_in,sFilename_mesh_in, sWorkspace_out):
    """
    prepare the flowline using multiple step approach
    """

    #step 1: convert it to json format
    sFilename_out = sWorkspace_out + slash + 'flowline.json'
    #convert_shapefile_to_json( sFilename_shapefile_in, sFilename_out)

    
    #step 3: split into segment
    sFilename_in = sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline_split.json'
    #split_flowline(sFilename_in,  sFilename_out)

    

    #connect disconnected vertex
    sFilename_in = sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline_connect.json'
    #sFilename_out = sWorkspace_out + slash + 'flowline_connect.shp'
    #connect_disconnect_line(sFilename_in,  sFilename_out )
    

    sFilename_in = sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline_vertex_without_confluence.json'
    #find_flowline_vertex(sFilename_in,  sFilename_out)

    #split again
    sFilename_in = sWorkspace_out + slash + 'flowline_connect.json'
    sFilename_in2 = sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline_split_by_point.json'
    #split_flowline3(sFilename_in, sFilename_in2, sFilename_out)

    sFilename_in = sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline_direction.json'
    #correct_flowline_direction(sFilename_in,  sFilename_out)
    

    #step 4: remove loops
    
    sFilename_in = sFilename_out    
    sFilename_out = sWorkspace_out + slash + 'flowline_loop.json'
    #remove_flowline_loop3(sFilename_in,  sFilename_out)    

    sFilename_in = sFilename_out    
    sFilename_out = sWorkspace_out + slash + 'flowline_large.json'
    #sFilename_in = sWorkspace_out + slash + 'flowline_large.shp'
    #remove_small_river(sFilename_in, sFilename_out, 1.0E4)
    
   
    
    sFilename_in = sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline_vertex_with_confluence.json'
    #find_flowline_vertex2(sFilename_in,  sFilename_out)
    
    sFilename_in = sWorkspace_out + slash + 'flowline_large.json'
    
    sFilename_in2 = sFilename_out

    sFilename_out = sWorkspace_out + slash + 'flowline_merge.json'
    #merge_flowline2(sFilename_in, sFilename_in2,  sFilename_out )    

    sFilename_in = sFilename_out    
    sFilename_out = sWorkspace_out + slash + 'flowline_large2.json'
    #remove_small_river(sFilename_in, sFilename_out, 1.0E4)

    sFilename_in = sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline_vertex_with_confluence2.json'
    #find_flowline_vertex2(sFilename_in,  sFilename_out)
    
    sFilename_in = sWorkspace_out + slash + 'flowline_large2.json'
    
    sFilename_in2 = sFilename_out

    sFilename_out = sWorkspace_out + slash + 'flowline_merge2.json'
    #merge_flowline2(sFilename_in, sFilename_in2,  sFilename_out )    
  
    #step 2: merge all as one single feature     
    #build stream order 
    sFilename_in = sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline_order.json'
    define_stream_order(sFilename_in, sFilename_out)
 

    #step 5: remove small headwater segment
    
    #step 6: intersect with mesh and simplify
    sFilename_mesh = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/hexagon.json'
    sFilename_flowline= sFilename_out
    sFilename_out = sWorkspace_out + slash + 'flowline_intersect.json'

    #intersect_flowline_with_mesh(sFilename_mesh, sFilename_flowline, sFilename_out)

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
