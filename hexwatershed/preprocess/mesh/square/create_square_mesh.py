#create a rectangle latitude/longitude based mesh
#we will use some GIS way to define it
#longitude left and latitude bottom and nrow and ncolumn and resolution is used to define the rectangle
#because it is mesh, it represent the edge instead of center
#we will use gdal api for most operations
import os, sys
from osgeo import ogr, osr, gdal, gdalconst

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
sPath_pye3sm='/people/liao313/workspace/python/hexwatershed/pyhexwatershed'
sys.path.append(sPath_pye3sm)

from hexwatershed.auxiliary.gdal_function import obtain_raster_metadata


os.environ['PROJ_LIB'] = '/qfs/people/liao313/.conda/envs/gdalenv/share/proj'

def create_square_mesh(dX_left, dY_bot, dResolution, ncolumn, nrow, sFilename_output, sFilename_shapefile):

   
    if os.path.exists(sFilename_output): 
        #delete it if it exists
        os.remove(sFilename_output)

    #pDriver = ogr.GetDriverByName('Esri Shapefile')
    pDriver = ogr.GetDriverByName('GeoJSON')
    #geojson
    pDataset = pDriver.CreateDataSource(sFilename_output)
    #pSpatialRef = osr.SpatialReference(wkt=pProjection)

    pDriver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
    pDataset_shapefile = pDriver_shapefile.Open(sFilename_shapefile, 0)
    pLayer_shapefile = pDataset_shapefile.GetLayer(0)
    pSrs = pLayer_shapefile.GetSpatialRef()

    #pDriver_geotiff = gdal.GetDriverByName('GTiff')    
    #pDataset_geotiff = gdal.Open(sFilename_geotiff, gdal.GA_ReadOnly)
    #pProjection = pDataset_geotiff.GetProjection()
    #pSrs = osr.SpatialReference(wkt=pProjection)

    pLayer = pDataset.CreateLayer('cell', pSrs, ogr.wkbPolygon)
    # Add one attribute
    pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn = pLayer.GetLayerDefn()
    pFeature = ogr.Feature(pLayerDefn)

    

    xleft = dX_left
    xspacing= dResolution
    ybottom = dY_bot
    yspacing = dResolution

    lID =0 
    #.........
    #(x2,y2)-----(x3,y3)
    #   |           |
    #(x1,y1)-----(x4,y4)
    #...............
    for column in range(0, ncolumn):
        for row in range(0, nrow):
            #define a polygon here
            x1 = xleft + (column * xspacing)
            y1 = ybottom + (row * yspacing)

            x2 = xleft + (column * xspacing)
            y2 = ybottom + ((row + 1) * yspacing)

            x3 = xleft + ((column + 1) * xspacing)
            y3 = ybottom + ((row + 1) * yspacing)

            x4 = xleft + ((column + 1) * xspacing)
            y4 = ybottom + (row * yspacing)
           

            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(x1, y1)
            ring.AddPoint(x2, y2)
            ring.AddPoint(x3, y3)
            ring.AddPoint(x4, y4)
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


    
    dResolution=40*1000.0
    
    

    #we can use the dem extent to setup 
    sFilename_geotiff = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/raster/dem/crbdem.tif'
    dPixelWidth, dOriginX, dOriginY, nrow, ncolumn, pSpatialRef, pPrejection = obtain_raster_metadata(sFilename_geotiff)
    
  

    
    dX_left = dOriginX

    dX_right = dOriginX + (ncolumn +1)* dPixelWidth

    dY_top = dOriginY

    dY_bot = dOriginY - (nrow +1)* dPixelWidth

    ncolumn= int( (dX_right - dX_left) / dResolution )
    nrow= int( (dY_top - dY_bot) / dResolution )

    
    sFilename_output = 'square_40k' + '.json'
    sWorkspace_out = '/compyfs/liao313/04model/pyhexwatershed/columbia_river_basin'

    sFilename_output = os.path.join(sWorkspace_out, sFilename_output)
    sFilename_shapefile = '/qfs/people/liao313/data/hexwatershed/columbia_river_basin/vector/mesh_id/crb_flowline_remove_small_line_split.shp'

    create_square_mesh(dX_left, dY_bot, dResolution, ncolumn, nrow, sFilename_output, sFilename_shapefile)

