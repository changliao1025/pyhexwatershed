import os, sys
import numpy as np
import osgeo
from osgeo import ogr, osr, gdal, gdalconst

gdal.UseExceptions()    # Enable exceptions


def reproject_coordinates(dx_in, dy_in, pSpatial_reference_source_in, pSpatial_reference_target_in=None):
    """ Reproject a pair of x,y coordinates. 

    Args:
        dx_in (float): X Coordinate of point
        dy_in (float): Y Coordinate of
        pSpatial_reference_source_in (osr): The source spatial reference of point
        pSpatial_reference_target_in (osr, optional): The target spatial reference of point. Defaults to None.

    Returns:
        Tuple: dx_new, dy_new
    """

    if pSpatial_reference_target_in is not None:

        pass
    else:
        pSpatial_reference_target_in = osr.SpatialReference()
        pSpatial_reference_target_in.ImportFromEPSG(4326)
        
        pass

    
    if int(osgeo.__version__[0]) >= 3:
    # GDAL 3 changes axis order: https://github.com/OSGeo/gdal/issues/1546
                    
        pSpatial_reference_source_in.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)
        pSpatial_reference_target_in.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)

    
    pTransform = osr.CoordinateTransformation( pSpatial_reference_source_in, pSpatial_reference_target_in)
   
    dx_out,dy_out, z = pTransform.TransformPoint( dx_in,dy_in)
    
    return dx_out, dy_out

def reproject_coordinates_batch(aX_in, aY_in, pSpatial_reference_source_in, pSpatial_reference_target_in=None):
    """ Reproject a list of x, y coordinates.

    Args:
        aX_in (list): A list of X Coordinate of points
        aY_in (list): A list of Y Coordinate of points
        pSpatial_reference_source_in (osr): The source spatial reference of point
        pSpatial_reference_target_in (osr, optional): The target spatial reference of point. Defaults to None.

    Returns:
        Tuple: aX_out, aY_out
    """

    if pSpatial_reference_target_in is not None:

        pass
    else:
        pSpatial_reference_target_in = osr.SpatialReference()
        pSpatial_reference_target_in.ImportFromEPSG(4326)
        
        pass

    
    if int(osgeo.__version__[0]) >= 3:
    # GDAL 3 changes axis order: https://github.com/OSGeo/gdal/issues/1546
                    
        pSpatial_reference_source_in.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)
        pSpatial_reference_target_in.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)

    
    pTransform = osr.CoordinateTransformation( pSpatial_reference_source_in, pSpatial_reference_target_in)

    npoint = len(aX_in)
    aX_out=list()
    aY_out=list()
    for i in range(npoint):
        x0 = aX_in[i]
        y0 = aY_in[i]
   
        x1,y1, z = pTransform.TransformPoint( x0,y0)

        aX_out.append(x1)
        aY_out.append(y1)
    
    return aX_out,aY_out

def obtain_raster_metadata_geotiff(sFilename_geotiff_in):
    """retrieve the metadata of a geotiff file

    Args:
        sFilename_geotiff (string): The filename of geotiff

    Returns:
       Tuple: dPixelWidth, dOriginX, dOriginY, nrow, ncolumn, pSpatial_reference, pProjection, pGeotransform
    """

    if os.path.exists(sFilename_geotiff_in):
        pass
    else:
        print('The file does not exist!')
        return
    
    sDriverName='GTiff'    
    pDriver = gdal.GetDriverByName(sDriverName)
    if pDriver is None:
        print ("%s pDriver not available.\n" % sDriverName)
    else:
        print  ("%s pDriver IS available.\n" % sDriverName) 
   
    pDataset = gdal.Open(sFilename_geotiff_in, gdal.GA_ReadOnly)

    if pDataset is None:
        print("Couldn't open this file: " + sFilename_geotiff_in)
        sys.exit("Try again!")
    else: 
        pProjection = pDataset.GetProjection()
        pSpatial_reference = osr.SpatialReference(wkt=pProjection)
    
    
        ncolumn = pDataset.RasterXSize
        nrow = pDataset.RasterYSize
        #nband = pDataset.RasterCount

        pGeotransform = pDataset.GetGeoTransform()
        dOriginX = pGeotransform[0]
        dOriginY = pGeotransform[3]
        dPixelWidth = pGeotransform[1]
        pPixelHeight = pGeotransform[5]       
        
        
        return dPixelWidth, dOriginX, dOriginY, nrow, ncolumn, pSpatial_reference, pProjection, pGeotransform

def obtain_shapefile_metadata(sFilename_shapefile_in):
    """
    Obtain the metadata of a shapefile

    Args:
        sFilename_shapefile (string): The filename of the shapefile

    Returns:
        Tuple: left_min, right_max, bot_min, top_max
    """
    if os.path.exists(sFilename_shapefile_in):
        pass
    else:
        print('The  shapefile does not exist!')
        return


    sDriverName='ESRI Shapefile'    
    pDriver_shapefile = ogr.GetDriverByName(sDriverName)
    if pDriver_shapefile is None:
        print ("%s pDriver not available.\n" % sDriverName)
    else:
        print  ("%s pDriver IS available.\n" % sDriverName) 
   
    pDataset = pDriver_shapefile.Open(sFilename_shapefile_in, gdal.GA_ReadOnly)
    pLayer = pDataset.GetLayer(0)
  

    if pDataset is None:
        print("Couldn't open this file: " + sFilename_shapefile_in)
        sys.exit("Try again!")
    else:    
        
        iFlag_first=1
    
        for feature in pLayer:
            pGeometry = feature.GetGeometryRef()
            pEnvelope = pGeometry.GetEnvelope()

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

        return left_min, right_max, bot_min, top_max

