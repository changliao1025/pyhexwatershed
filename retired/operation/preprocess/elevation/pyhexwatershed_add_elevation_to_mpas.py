
import sys
import argparse
sPath_rtop = '/qfs/people/liao313/workspace/python/rtopodem/'
sys.path.append(sPath_rtop)


from dem_remap import dem_remap
from dem_trnsf import dem_trnsf
def pyhexwatershed_add_elevation_to_mpas( sFilename_dem, sFilename_base_mesh,sFilename_invert_mesh):

    #dem_remap( sFilename_dem,sFilename_base_mesh)

    dem_trnsf(sFilename_base_mesh, sFilename_invert_mesh )


    return


if (__name__ == "__main__"):

    
    sFilename_dem = '/compyfs/liao313/00raw/dem/global/mpas/RTopo_2_0_4_GEBCO_v2020_30sec_pixel.nc'
    sFilename_base_mesh = '/people/liao313/workspace/python/jigsaw/icom-mesh/mesh/delaware_60_30_5_2_w_boundary/out/base_mesh.nc'
    sFilename_invert_mesh = '/people/liao313/workspace/python/jigsaw/icom-mesh/mesh/delaware_60_30_5_2_w_boundary/out/invert_mesh.nc'
    pyhexwatershed_add_elevation_to_mpas(sFilename_dem, sFilename_base_mesh, sFilename_invert_mesh)