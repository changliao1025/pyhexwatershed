import os, sys
from osgeo import ogr, osr, gdal, gdalconst
import numpy as np
from hexwatershed.preprocess.stream.check_same_point  import check_same_point
def find_vertex_in_list(aPt, pt):
    index= -1
    npt= len(aPt)
    if npt>0:
        for i in range(npt):
            if( check_same_point(pt, aPt[i]) ==1 ):
                index = i
                break
    else:
        return -1
    return index