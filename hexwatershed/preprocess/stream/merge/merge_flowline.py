import os, sys
from osgeo import ogr, osr, gdal, gdalconst
import numpy as np


from hexwatershed.preprocess.stream.check_same_point  import check_same_point
def merge_flowline(sFilename_in, sFilename_out):
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

    newGeometry = None
    lID =0
    for pFeature_in in pLayer_in:
        pGeometry_in = pFeature_in.GetGeometryRef()
        if newGeometry is None:
           newGeometry = pGeometry_in.Clone()
        else:
           newGeometry = newGeometry.Union(pGeometry_in)

    #print (newGeometry)

    pFeature_out.SetGeometry(newGeometry)
    pFeature_out.SetField("id", lID)
        
    # Add new pFeature_shapefile to output Layer
    pLayer_out.CreateFeature(pFeature_out)        
    pDataset_out.FlushCache()
    
    pDataset_out = pLayer_out = pFeature_out = None    

    return 

def merge_flowline2(sFilename_in, sFilename_out):
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
    nfeature = pLayer_in.GetFeatureCount()
    aFlag = np.full(nfeature, 0,dtype=int)

    lID = 0
    def check_head_water(pt):
        iCount=0
        for i in range(0, nfeature):      
            pFeature_in = pLayer_in.GetFeature(i)
            pGeometry_in = pFeature_in.GetGeometryRef()
            npoint = pGeometry_in.GetPointCount()        
            pt_start = pGeometry_in.GetPoint(0)
            pt_end = pGeometry_in.GetPoint(npoint-1)
            if( check_same_point( pt_start,pt )  ==1):
                iCount = iCount +1
            
            if( check_same_point( pt_end,pt )  ==1):
                iCount = iCount +1

        if iCount == 1:
            return 1
        else:
            return 0
    for i in range(0, nfeature):      
        pFeature_in = pLayer_in.GetFeature(i)
        pGeometry_in = pFeature_in.GetGeometryRef()
        npoint = pGeometry_in.GetPointCount()        
        pt_start = pGeometry_in.GetPoint(0)
        pt_end = pGeometry_in.GetPoint(npoint-1)

       

        if( aFlag[i] ==0 ):
            if (check_head_water(pt_start  ) ==1):
                #search all the linked points


                pass
            else:
                if (check_head_water(pt_end  ) ==1):
                    pass

                pass

            pass
        else:
            pass
        
       


    pFeature_out.SetField("id", lID)
        
    # Add new pFeature_shapefile to output Layer
    pLayer_out.CreateFeature(pFeature_out)        
    pDataset_out.FlushCache()
    
    pDataset_out = pLayer_out = pFeature_out = None    

    return 
