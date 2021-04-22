import os, sys

from pyearth.system.define_global_variables import *
from hexwatershed.preprocess.stream.simplification.json.remove_flowline_loop_json import remove_flowline_loop_json
def simplify_flowline(sFilename_mesh_in, sFilename_flowline_in, sFilename_output_out):
    """
    pre-process the flowline so it can be used in hexwatershed
    
    """

    sFilename_output_out = os.path.basename(sFilename_flowline_in) + slash + '_step1.json'

    remove_flowline_loop_json(sFilename_flowline_in, sFilename_output_out)

    return


if __name__ == '__main__':
    sFilename_mesh = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/hexagon.json'

  
    sFilename_flowline = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/flowline.json'
    sFilename_output = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/flowline_intersect_hexagon.json'

    simplify_flowline(sFilename_mesh, sFilename_flowline, sFilename_output)