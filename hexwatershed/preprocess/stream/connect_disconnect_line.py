
import os, sys
import numpy as np 
from osgeo import ogr, osr, gdal, gdalconst

def calculate_point_distance(pt1, pt2):
    x1=pt1[0]
    y1=pt1[1]
    x2=pt2[0]
    y2=pt2[1]
    dDistance = np.power(  (x2 - x1 ) ,2)  + np.power(  (y2 - y1 ) ,2)        
    dDistance = np.sqrt(dDistance)    
    return dDistance
def connect_disconnect_line(sFilename_in, sFilename_out):
    if  os.path.exists(sFilename_in): 
        pass
    else: 
        print('The input file does not exist')
        return
        
    if os.path.exists(sFilename_out): 
        #delete it if it exists
        os.remove(sFilename_out)

    pDriver = ogr.GetDriverByName('GeoJSON')
    #geojson
    pDataset_out = pDriver.CreateDataSource(sFilename_out)
    pDataset_in = pDriver.Open(sFilename_in, gdal.GA_ReadOnly)
    pLayer_in = pDataset_in.GetLayer(0)
    pSpatialRef_in = pLayer_in.GetSpatialRef()
    

    pLayer_out = pDataset_out.CreateLayer('flowline', pSpatialRef_in, ogr.wkbLineString)
    # Add one attribute
    pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn_out = pLayer_out.GetLayerDefn()
    pFeature_out = ogr.Feature(pLayerDefn_out)

   
    lID =0

    pointa = [-1568732.491,3064177.639]
    pointb = [-1589612.188,3068975.112]
    for pFeature_in in pLayer_in:
        pGeometry_in = pFeature_in.GetGeometryRef()
        npoint = pGeometry_in.GetPointCount()      
        #print(pGeometry_in.GetGeometryName())
        pt_start = pGeometry_in.GetPoint(0)
        pt_end = pGeometry_in.GetPoint(npoint-1)

        line = ogr.Geometry(ogr.wkbLineString)

        dis1 = calculate_point_distance(pt_start,pointa )
        dis2 = calculate_point_distance(pt_end,pointa )
        if dis1 < 300:
            line.AddPoint(pointa[0], pointa[1])
            pass

        dis3 = calculate_point_distance(pt_start,pointb )
        dis4 = calculate_point_distance(pt_end,pointb )
        if dis3 < 300:
            line.AddPoint(pointb[0], pointb[1])
            pass        

        for j in range(0,npoint):
            point = pGeometry_in.GetPoint(j)                          
            line.AddPoint(point[0], point[1])
            
        
        if dis2 < 300:
            line.AddPoint(pointa[0], pointa[1])
            pass
        if dis4 < 300:
            line.AddPoint(pointb[0], pointb[1])
            pass


        pFeature_out.SetGeometry(line)
        pFeature_out.SetField("id", lID)
        pLayer_out.CreateFeature(pFeature_out)        
        lID= lID+1
        
    # Add new pFeature_shapefile to output Layer
    
    pDataset_out.FlushCache()
    
    pDataset_out = pLayer_out = pFeature_out = None    

    return 