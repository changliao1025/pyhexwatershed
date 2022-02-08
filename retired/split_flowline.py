import os, sys
from osgeo import ogr, osr, gdal, gdalconst

from hexwatershed.preprocess.stream.add_unique_point import add_unique_point

import numpy as np

def check_same_point(x1, y1, x2, y2):
    a = (x1-x2) *(x1-x2)
    b= (y1-y2) *(y2-y2)
    c = np.sqrt(a+b)
    if( c < 0.0000001 ):
        return 1
    else:
        return 0


def split_flowline(sFilename_in, sFilename_out):

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
    

    pLayer_out = pDataset_out.CreateLayer('flowline', pSpatialRef_in, ogr.wkbMultiLineString)
    # Add one attribute
    pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn_out = pLayer_out.GetLayerDefn()
    pFeature_out = ogr.Feature(pLayerDefn_out)

    
    lID =0
    for pFeature_in in pLayer_in:
        pGeometry_in = pFeature_in.GetGeometryRef()
        aLine = ogr.ForceToLineString(pGeometry_in)
        for Line in aLine: 
            pFeature_out.SetGeometry(Line)
            pFeature_out.SetField("id", lID)
            lID = lID + 1
        
            # Add new pFeature_shapefile to output Layer
            pLayer_out.CreateFeature(pFeature_out)        
    
    pDataset_out.FlushCache()
    pDataset_out = pLayer_out = pFeature_out = None    

    return 

def find_flowline_vertex(sFilename_in, sFilename_out):
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
    

    pLayer_out = pDataset_out.CreateLayer('vertex', pSpatialRef_in, ogr.wkbPoint)
    # Add one attribute
    pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn_out = pLayer_out.GetLayerDefn()
    pFeature_out = ogr.Feature(pLayerDefn_out)

    
    lID = 0
    aDic =[]
    for pFeature_in in pLayer_in:
        pGeometry_in = pFeature_in.GetGeometryRef()
        npoint = pGeometry_in.GetPointCount()
        pPoint_start=pGeometry_in.GetPoint(0)
        pPoint_end=pGeometry_in.GetPoint(npoint-1)        
        add_unique_point(aDic, pPoint_start)
        add_unique_point(aDic, pPoint_end)
    
    for i in range(len( aDic ) ):
        pPoint = aDic[i]
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(pPoint[0], pPoint[1])
        pFeature_out.SetGeometry(point)
        pFeature_out.SetField("id", lID)
        lID = lID + 1    
        pLayer_out.CreateFeature(pFeature_out)        
    
    pDataset_out.FlushCache()
    pDataset_out = pLayer_out = pFeature_out = None    
    return

def split_flowline2(sFilename_in1, sFilename_in2, sFilename_out):

    if  os.path.exists(sFilename_in1): 
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
    pDataset_in1 = pDriver.Open(sFilename_in1, gdal.GA_ReadOnly)
    pLayer_in1 = pDataset_in1.GetLayer(0)
    pDataset_in2 = pDriver.Open(sFilename_in2, gdal.GA_ReadOnly)
    pLayer_in2 = pDataset_in2.GetLayer(0)
    pSpatialRef_in = pLayer_in1.GetSpatialRef()
    
    pLayer_out = pDataset_out.CreateLayer('flowline', pSpatialRef_in, ogr.wkbLineString)
    # Add one attribute
    pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn_out = pLayer_out.GetLayerDefn()
    pFeature_out = ogr.Feature(pLayerDefn_out)

    lID =0
    nfeature1 = pLayer_in1.GetFeatureCount()
    nfeature2 = pLayer_in2.GetFeatureCount()
    for i in range(0, nfeature1):    
        pFeature1= pLayer_in1.GetFeature(i)
        pGeometry1 = pFeature1.GetGeometryRef()        
        print(pGeometry1.GetGeometryName())
        for j in range(0, nfeature2):
            pFeature2= pLayer_in2.GetFeature(j)
            pGeometry2 = pFeature2.GetGeometryRef()
            print(pGeometry2.GetGeometryName())
            if (pGeometry2.IsValid()):
                pass
            else:
                print('Geometry issue')
      
            iFlag_intersect = pGeometry2.Intersects( pGeometry1 )
            if( iFlag_intersect == True):
                pGeometry3 = pGeometry2.Intersection(pGeometry1) 
                print(pGeometry3.GetGeometryName())
                pFeature_out.SetGeometry(pGeometry3)
                pFeature_out.SetField("id", lID)                
                pFeature_out.CreateFeature(pFeature_out)    
                lID = lID + 1

            else:
                pass    
    
    pDataset_out.FlushCache()
    pDataset_out = pLayer_out = pFeature_out = None    

    return 

def split_flowline2_old(sFilename_in, sFilename_in2, sFilename_out):

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
    

    pLayer_out = pDataset_out.CreateLayer('flowline', pSpatialRef_in, ogr.wkbMultiLineString)
    # Add one attribute
    pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn_out = pLayer_out.GetLayerDefn()
    pFeature_out = ogr.Feature(pLayerDefn_out)

    def check_on_other_line_middle(x, y):
        for k in range(0, nfeature):
            pFeature_in = pLayer_in.GetFeature(k)
            pGeometry_in = pFeature_in.GetGeometryRef()
            npoint = pGeometry_in.GetPointCount()
            pPoint_start=pGeometry_in.GetPoint(0)
            pPoint_end=pGeometry_in.GetPoint(npoint-1)
            x1 = pPoint_start[0]
            y1 = pPoint_start[1]
            x2 = pPoint_end[0]
            y2 = pPoint_end[1]
            iFlag0 =  check_same_point(x, y, x1,y1)
            iFlag1 =  check_same_point(x, y, x2,y2)
            if( iFlag0 == 1 or iFlag1 ==1):
                return 1

        return 0

    lID =0
    nfeature = pLayer_in.GetFeatureCount()
    for j in range(0, nfeature):
        print(j)
        pFeature_in = pLayer_in.GetFeature(j)
        pGeometry_in = pFeature_in.GetGeometryRef()
        npoint = pGeometry_in.GetPointCount()
        
        iFlag_single = 1
        for i in range(1, npoint-1):               
            pPoint = pGeometry_in.GetPoint(i)
            x = pPoint[0]
            y = pPoint[1]      
            iFlag0 = check_on_other_line_middle(x, y)
        
            #find 
            if(iFlag0==1):
                #we need to break it
                iFlag_single =0
                break
            else:
                iFlag_single =1

        if (iFlag_single ==1):

            pFeature_out.SetGeometry(pGeometry_in)
            pFeature_out.SetField("id", lID)
            lID = lID + 1        
            # Add new pFeature_shapefile to output Layer
            pLayer_out.CreateFeature(pFeature_out)        
        else:
            print('break')
      
        

    
    pDataset_out.FlushCache()
    pDataset_out = pLayer_out = pFeature_out = None    

    return 