#create a rectangle latitude/longitude based mesh
#we will use some GIS way to define it
#longitude left and latitude bottom and nrow and ncolumn and resolution is used to define the rectangle
#because it is mesh, it represent the edge instead of center
#we will use gdal api for most operations
import os, sys
import numpy as np
from osgeo import ogr, osr, gdal, gdalconst

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
sPath_pye3sm='/people/liao313/workspace/python/hexwatershed/pyhexwatershed'
sys.path.append(sPath_pye3sm)

from hexwatershed.auxiliary.gdal_function import obtain_raster_metadata
from hexwatershed.auxiliary.gdal_function import reproject_coordinates
from hexwatershed.auxiliary.degree_to_meter import degree_to_meter

def create_hexagon_mesh(dX_left, dY_bot, dResolution, ncolumn, nrow, sFilename_output, sFilename_shapefile):

    
    if os.path.exists(sFilename_output): 
        #delete it if it exists
        os.remove(sFilename_output)

    #pDriver = ogr.GetDriverByName('Esri Shapefile')
    pDriver = ogr.GetDriverByName('GeoJSON')
    #geojson
    pDataset = pDriver.CreateDataSource(sFilename_output)
    
    pDriver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
    pDataset_shapefile = pDriver_shapefile.Open(sFilename_shapefile, 0)
    pLayer_shapefile = pDataset_shapefile.GetLayer(0)
    pSrs = pLayer_shapefile.GetSpatialRef()

    pLayer = pDataset.CreateLayer('cell', pSrs, ogr.wkbPolygon)
    # Add one attribute
    pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn = pLayer.GetLayerDefn()
    pFeature = ogr.Feature(pLayerDefn)

    

    xleft = dX_left
    ybottom = dY_bot

    dArea = np.power(dResolution_meter,2.0)
    #hexagon edge
    dLength_edge = np.sqrt(  2.0 * dArea / (3.0* np.sqrt(3.0))  )
    dX_shift = 0.5 * dLength_edge
    dY_shift = 0.5 * dLength_edge * np.sqrt(3.0)
    dX_spacing = dLength_edge * 1.5
    dY_spacing = dLength_edge * np.sqrt(3.0)

    lID =0 
    #.........
    #(x2,y2)-----(x3,y3)
    #   |           |
    #(x1,y1)-----(x4,y4)
    #...............
    for column in range(0, ncolumn):
        for row in range(0, nrow):
            if column % 2 == 0 :
            #define a polygon here
                x1 = xleft + (column * dX_spacing)
                y1 = ybottom + (row * dY_spacing)
            else:
                x1 = xleft + (column * dX_spacing) #- dX_shift
                y1 = ybottom + (row * dY_spacing) - dY_shift


            x2 = x1 - dX_shift
            y2 = y1 + dY_shift

            x3 = x1 
            y3 = y1 + dY_shift * 2.0

            x4 = x1 + dLength_edge
            y4 = y1 + dY_shift * 2.0

            x5 = x4 + dX_shift
            y5 = y1 + dY_shift

            x6 = x1 + dLength_edge
            y6 = y1         
           

            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(x1, y1)
            ring.AddPoint(x2, y2)
            ring.AddPoint(x3, y3)
            ring.AddPoint(x4, y4)
            ring.AddPoint(x5, y5)
            ring.AddPoint(x6, y6)
            ring.AddPoint(x1, y1)
            pPolygon = ogr.Geometry(ogr.wkbPolygon)
            pPolygon.AddGeometry(ring)

            pFeature.SetGeometry(pPolygon)
            pFeature.SetField("id", lID)
            pLayer.CreateFeature(pFeature)

            lID = lID + 1


            pass
    pDataset = pLayer = pFeature  = None      



    return


if __name__ == '__main__':
    dResolution=0.5
   
    

    #we can use the dem extent to setup 
    sFilename_geotiff = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/raster/dem/crbdem.tif'
    dPixelWidth, dOriginX, dOriginY, nrow, ncolumn, pSpatialRef, pProjection = obtain_raster_metadata(sFilename_geotiff)
    
    spatial_reference_source = pSpatialRef
    spatial_reference_target = osr.SpatialReference()  
    spatial_reference_target.ImportFromEPSG(4326)

    dY_bot = dOriginY - (nrow+1) * dPixelWidth
    dLongitude_left,  dLatitude_bot= reproject_coordinates(dOriginX, dY_bot,spatial_reference_source,spatial_reference_target)

    dX_right = dOriginX + (ncolumn +1) * dPixelWidth
    

    dLongitude_right, dLatitude_top= reproject_coordinates(dX_right, dOriginY,spatial_reference_source,spatial_reference_target)

    dLatitude_mean = 0.5 * (dLatitude_top + dLatitude_bot)

    dResolution_meter = degree_to_meter(dLatitude_mean, dResolution )


    dX_left = dOriginX
    dY_top = dOriginY

    dArea = np.power(dResolution_meter,2.0)
    #hexagon edge
    dLength_edge = np.sqrt(  2.0 * dArea / (3.0* np.sqrt(3.0))  )
    dLength_shift = 0.5 * dLength_edge * np.sqrt(3.0)
    dX_spacing = dLength_edge * 1.5
    dY_spacing = dLength_edge * np.sqrt(3.0)

   
    ncolumn= int( (dX_right - dX_left) / dX_spacing )
    nrow= int( (dY_top - dY_bot) / dY_spacing )


    sFilename_output = 'hexagon.json'
    sWorkspace_out = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin'

    sFilename_output = os.path.join(sWorkspace_out, sFilename_output)
    sFilename_shapefile = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/vector/mesh_id/crb_flowline_remove_small_line_split.shp'
    create_hexagon_mesh(dX_left, dY_bot, dResolution_meter, ncolumn, nrow, sFilename_output, sFilename_shapefile)

