
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
def world2Pixel(geoMatrix, x, y):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the pixel location of a geospatial coordinate
    """
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    pixel = int((x - ulX) / xDist)
    line = int((ulY - y) / xDist)
    return (pixel, line)

def obtain_elevation_based_on_mesh(sFilename_mesh, sFilename_elevation, sFilename_output):
    sFilename_clip =  '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/clip.tif'

    pDriver_memory = gdal.GetDriverByName('MEM')
    pDriver_geotiff = gdal.GetDriverByName('GTiff')
    if os.path.exists(sFilename_output): 
        #delete it if it exists
        os.remove(sFilename_output)
    
   
    pDataset_elevation = gdal.Open(sFilename_elevation, gdal.GA_ReadOnly)

    dPixelWidth, dOriginX, dOriginY, nrow, ncolumn, pSpatialRef, pProjection, pGeotransform = obtain_raster_metadata(sFilename_geotiff)

    geoTrans = pGeotransform
    pSpatialRef_target = pSpatialRef
    pDriver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
    pDriver_json = ogr.GetDriverByName('GeoJSON')
    
    pDataset_mesh = pDriver_json.Open(sFilename_mesh, gdal.GA_ReadOnly)
    #pDataset_out = pDriver_json.Open(sFilename_output, gdal.GA_Update)
    pDataset_out = pDriver_json.CreateDataSource(sFilename_output)

    if pDataset_elevation is None or pDataset_mesh is None:
        print("Couldn't open this file: " + sFilename_elevation)
        sys.exit("Try again!")
        pass
    else: 
        #
        pLayer1 = pDataset_mesh.GetLayer(0)
        
        pSpatialRef1 = pLayer1.GetSpatialRef()

        pLayer2 = pDataset_out.CreateLayer('cell', pSpatialRef1, ogr.wkbPolygon)
        pLayer2.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64))
        pLayer2.CreateField(ogr.FieldDefn('elev', ogr.OFTReal))
        pLayerDefn = pLayer2.GetLayerDefn()
        pFeature2 = ogr.Feature(pLayerDefn)
        lID =0 
        for pFeature1 in pLayer1:       
            pGeometry1 = pFeature1.GetGeometryRef()           

            pEnvelope = pGeometry1.GetEnvelope()
            minX, maxX, minY, maxY = pGeometry1.GetEnvelope()

            ulX, ulY = world2Pixel(geoTrans, minX, maxY)
            lrX, lrY = world2Pixel(geoTrans, maxX, minY)
            iBeginRow = 0
            iBeginCol = 0

            iNewWidth = int( (maxX - minX) / abs(dPixelWidth)  )
            iNewHeigh = int( (maxY - minY) / abs(dPixelWidth) )
            newGeoTransform = (minX, dPixelWidth, 0,    maxY, 0, -dPixelWidth)            

            pDataset_clip = pDriver_memory.Create('', iNewWidth, iNewHeigh, 1, gdalconst.GDT_Float32)
            pDataset_clip.SetGeoTransform( newGeoTransform )
            pDataset_clip.SetProjection( pProjection)

            pDataset3 = pDriver_shapefile.CreateDataSource('/vsimem/memory_name.shp')
            pLayerOut = pDataset3.CreateLayer('cell', pSpatialRef1, ogr.wkbPolygon)    
            pLayerDefn = pLayerOut.GetLayerDefn()
            pFeatureOut = ogr.Feature(pLayerDefn)
            pFeatureOut.SetGeometry(pGeometry1)  
            pLayerOut.CreateFeature(pFeatureOut)    
            pDataset3.FlushCache()

            pWrapOption = gdal.WarpOptions(   cropToCutline=True,cutlineDSName   = '/vsimem/memory_name.shp' , \
                    width=iNewWidth,   \
                        height=iNewHeigh,      \
                            dstSRS=pProjection , format = 'MEM' )
            pDataset_clip = gdal.Warp('',pDataset_elevation, options=pWrapOption)

            pBand = pDataset_clip.GetRasterBand( 1 )
            dMissing_value = pBand.GetNoDataValue()
            aData_out = pBand.ReadAsArray(0,0,iNewWidth, iNewHeigh)
            #print(np.max(aData_out))
            aElevation = aData_out[np.where(aData_out !=dMissing_value)]

            pFeature2.SetGeometry(pGeometry1)
            pFeature2.SetField("id", lID)
            
            if(len(aElevation) >0 and np.mean(aElevation)!=-9999):
                #print(np.mean(aElevation))
                pFeature2.SetField("elev", np.mean(aElevation))
                pLayer2.CreateFeature(pFeature2)
                lID = lID + 1
                
            else:

                pFeature2.SetField("elev", -9999.0)

            
        pass



    pDataset_mesh.FlushCache()
    pDataset_mesh = pLayer1 = pFeature1  = None      

    return
if __name__ == '__main__':
    sFilename_mesh = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/hexagon.json'

  
    sFilename_flowline = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/flowline.json'
    sFilename_output = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin/hexagon_with_elevation.json'
    sFilename_geotiff = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/raster/dem/crbdem.tif'
   
    obtain_elevation_based_on_mesh(sFilename_mesh, sFilename_geotiff, sFilename_output)