
import os, sys
import json
import numpy as np
from osgeo import gdal, ogr, osr, gdalconst

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
sPath_pye3sm='/people/liao313/workspace/python/hexwatershed/pyhexwatershed'
sys.path.append(sPath_pye3sm)
os.environ['PROJ_LIB'] = '/qfs/people/liao313/.conda/envs/gdalenv/share/proj'
from hexwatershed.auxiliary.gdal_function import obtain_raster_metadata

def obtain_elevation_based_on_mesh(sFilename_mesh, sFilename_elevation):
    sFilename_clip =  '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/clip.tif'

    pDriver_memory = gdal.GetDriverByName('MEM')
    pDriver_geotiff = gdal.GetDriverByName('GTiff')
   
    pDataset_elevation = gdal.Open(sFilename_elevation, gdal.GA_ReadOnly)

    dPixelWidth, dOriginX, dOriginY, nrow, ncolumn, pSpatialRef, pProjection = obtain_raster_metadata(sFilename_geotiff)
    pSpatialRef_target = pSpatialRef
    pDriver_json = ogr.GetDriverByName('GeoJSON')
    pDataset_mesh = pDriver_json.Open(sFilename_mesh, gdal.GA_ReadOnly)

    if pDataset_elevation is None or pDataset_mesh is None:
        print("Couldn't open this file: " + sFilename_elevation)
        sys.exit("Try again!")
        pass
    else: 
        #
        pLayer1 = pDataset_mesh.GetLayer(0)
        for pFeature1 in pLayer1:       
            pGeometry1 = pFeature1.GetGeometryRef()

            pEnvelope = pGeometry1.GetEnvelope()
            minX, maxX, minY, maxY = pGeometry1.GetEnvelope()
            iBeginRow = 0
            iBeginCol = 0


            iNewWidth = int( (maxX - minX) / abs(dPixelWidth)  )
            iNewHeigh = int( (maxY - minY) / abs(dPixelWidth) )
            newGeoTransform = (minX, dPixelWidth, 0,    maxY, 0, -dPixelWidth)
            

            #pDataset_clip = pDriver_geotiff.Create('./clip.tif', iNewWidth, iNewHeigh, 1, gdalconst.GDT_Float32)
            #pDataset_clip.SetGeoTransform( newGeoTransform )
            #pDataset_clip.SetProjection( pProjection)

         
            pWrapOption = gdal.WarpOptions(   cropToCutline=True,cutlineLayer= pGeometry1 , \
                    width=iNewWidth,   \
                        height=iNewHeigh,      \
                            dstSRS=pProjection  )# format = 'MEM' , \
            pDataset_clip = gdal.Warp(destNameOrDestDS = sFilename_clip,srcDSOrSrcDSTab = pDataset_elevation, options=pWrapOption)

            pBand = pDataset_clip.GetRasterBand( 1 )
            dMissing_value = pBand.GetNoDataValue()
            aData_out = pBand.ReadAsArray(0,0,iNewWidth, iNewHeigh)
            print(np.max(aData_out))

        pass



    

    return
if __name__ == '__main__':
    sFilename_mesh = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/hexagon.json'

  
    sFilename_flowline = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/flowline.json'
    sFilename_output = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/flowline_intersect_hexagon.json'
    sFilename_geotiff = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/raster/dem/crbdem.tif'
   
    obtain_elevation_based_on_mesh(sFilename_mesh, sFilename_geotiff)