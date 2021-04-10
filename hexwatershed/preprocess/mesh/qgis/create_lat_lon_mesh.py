#create a rectangle latitude/longitude based mesh
#we will use some GIS way to define it
#longitude left and latitude bottom and nrow and ncolumn and resolution is used to define the rectangle
#because it is mesh, it represent the edge instead of center
#we will use gdal api for most operations
import os
from osgeo import ogr, osr, gdal, gdalconst

os.environ['PROJ_LIB'] = '/qfs/people/liao313/.conda/envs/gdalenv/share/proj'

def create_lat_lon_mesh(dLongitude_left, dLatitude_bot, dResolution, ncolumn, nrow):

    sResolution = '0.5'
    sFilename_output = 'MOSART_'+ sResolution + '.json'
    sWorkspace_out = '/compyfs/liao313/04model/hexwatershed/'

    sFilename_output = os.path.join(sWorkspace_out, sFilename_output)
    #pDriver = ogr.GetDriverByName('Esri Shapefile')
    pDriver = ogr.GetDriverByName('GeoJSON')
    #geojson
    pDataset = pDriver.CreateDataSource(sFilename_output)
    pSrs = osr.SpatialReference()  
    pSrs.ImportFromEPSG(4326)    # WGS84 lat/lon

    pLayer = pDataset.CreateLayer('cell', pSrs, ogr.wkbPolygon)
    # Add one attribute
    pLayer.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn = pLayer.GetLayerDefn()
    pFeature = ogr.Feature(pLayerDefn)

    

    xleft = dLongitude_left
    xspacing= dResolution
    ybottom = dLatitude_bot
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
    dLongitude_left= -180 
    dLatitude_bot=-90
    dResolution=0.5

    dLongitude_right = 180
    dLatitude_top = 90
    ncolumn= int( (dLongitude_right - dLongitude_left) / dResolution )
    nrow= int( (dLatitude_top - dLatitude_bot) / dResolution )

    create_lat_lon_mesh(dLongitude_left, dLatitude_bot, dResolution, ncolumn, nrow)

