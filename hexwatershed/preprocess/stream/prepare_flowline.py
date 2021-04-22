import os, sys
from pyearth.system.define_global_variables import *

from hexwatershed.preprocess.convert_shapefile_to_json import convert_shapefile_to_json
from hexwatershed.preprocess.stream.merge.merge_flowline import merge_flowline
def prepare_flowline(sFilename_shapefile_in,sFilename_mesh_in, sWorkspace_out):
    """
    prepare the flowline using multiple step approach
    """

    #step 1: convert it to json format
    sFilename_json_out = sWorkspace_out + slash + 'flowline1.json'
    convert_shapefile_to_json( sFilename_shapefile_in, sFilename_json_out)
    #step 1: merge all as one single feature
    sFilename_in = sFilename_json_out
    sFilename_out = sWorkspace_out + slash + 'flowline2.json'

    merge_flowline(sFilename_in,  sFilename_out )
    #step 2: split into segment
    #step 3: remove loops
    #step 4: remove small headwater segment
    #step 5: intersect with mesh and simplify
    #step 6: rebuild index and order
    #step 7: calculate proprities

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
