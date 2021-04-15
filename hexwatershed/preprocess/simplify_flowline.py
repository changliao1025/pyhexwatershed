#simplify flowline 
#decide to do it in C++ because it is easier for now
def simplify_flowline():


    return


if __name__ == '__main__':
    sFilename_mesh = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/hexagon.json'

  
    sFilename_flowline = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/flowline.json'
    sFilename_output = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/flowline_intersect_hexagon.json'

    simplify_flowline(sFilename_mesh, sFilename_flowline, sFilename_output)