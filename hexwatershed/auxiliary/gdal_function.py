import os, sys
import numpy as np
import osgeo
from osgeo import ogr, osr, gdal, gdalconst


os.environ['PROJ_LIB'] = '/qfs/people/liao313/.conda/envs/gdalenv/share/proj'



def reproject_coordinates(x, y, spatial_reference_source,spatial_reference_target):
    """ Reproject a list of x,y coordinates. """
    
    if int(osgeo.__version__[0]) >= 3:
    # GDAL 3 changes axis order: https://github.com/OSGeo/gdal/issues/1546
                    
        spatial_reference_source.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)
        spatial_reference_target.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)

    
    transform = osr.CoordinateTransformation( spatial_reference_source, spatial_reference_target)
    x_new,y_new, z = transform.TransformPoint(x, y)
    
    return x_new,y_new

def obtain_raster_metadata(sFilename_geotiff):
    pDriver = gdal.GetDriverByName('GTiff')
   
    pDataset = gdal.Open(sFilename_geotiff, gdal.GA_ReadOnly)

    if pDataset is None:
        print("Couldn't open this file: " + sFilename_geotiff)
        sys.exit("Try again!")
    else: 
        pProjection = pDataset.GetProjection()
        pSpatialRef = osr.SpatialReference(wkt=pProjection)
    
    
        ncolumn = pDataset.RasterXSize
        nrow = pDataset.RasterYSize
        #nband = pDataset.RasterCount

        pGeotransform = pDataset.GetGeoTransform()
        dOriginX = pGeotransform[0]
        dOriginY = pGeotransform[3]
        dPixelWidth = pGeotransform[1]
        pPixelHeight = pGeotransform[5]       
        
        print( dPixelWidth, dOriginX, dOriginY, nrow, ncolumn)
        return dPixelWidth, dOriginX, dOriginY, nrow, ncolumn, pSpatialRef, pProjection, pGeotransform

def obtain_shapefile_metadata(sFilename_shapefile):


    pDriver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
   
    pDataset = pDriver_shapefile.Open(sFilename_shapefile, gdal.GA_ReadOnly)
    pLayer = pDataset.GetLayer(0)
    #pSrs = pLayer.GetSpatialRef()

    if pDataset is None:
        print("Couldn't open this file: " + sFilename_shapefile)
        sys.exit("Try again!")
    else:    
        
        iFlag_first=1
    
        for feature in pLayer:
            pGeometry = feature.GetGeometryRef()
            pEnvelope = pGeometry.GetEnvelope()

            #"minX: %d, minY: %d, maxX: %d, maxY: %d" %(env[0],env[2],env[1],env[3])

            if iFlag_first ==1:
                left_min = pEnvelope[0]
                right_max =  pEnvelope[1]
                bot_min =  pEnvelope[2]
                top_max =  pEnvelope[3]
                iFlag_first = 0
            else:
                left_min = np.min([left_min,  pEnvelope[0]])
                right_max = np.max([right_max,  pEnvelope[1]])
                bot_min = np.min([bot_min,  pEnvelope[2]])
                top_max = np.max([top_max,  pEnvelope[3]])

        

            print( pEnvelope )
        print(left_min, right_max, bot_min, top_max)
        return left_min, right_max, bot_min, top_max

if __name__ == '__main__':
    sFilename_shapefile = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/vector/mesh_id/crb_flowline_remove_small_line_split.shp'
    obtain_shapefile_metadata(sFilename_shapefile)


    sFilename_geotiff = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/raster/dem/crbdem.tif'
    obtain_raster_metadata(sFilename_geotiff)