import os, sys
from osgeo import ogr, osr, gdal, gdalconst
import numpy as np


from hexwatershed.preprocess.stream.check_same_point  import check_same_point

def merge_flowline(sFilename_flowline_in, sFilename_out):
    if  os.path.exists(sFilename_flowline_in) and os.path.exists(sFilename_confluence_in): 
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
    pDataset_in1 = pDriver.Open(sFilename_flowline_in, gdal.GA_ReadOnly)
    pLayer_in1 = pDataset_in1.GetLayer(0)
    pSpatialRef_in = pLayer_in1.GetSpatialRef()    

    pDataset_in2 = pDriver.Open(sFilename_confluence_in, gdal.GA_ReadOnly)
    pLayer_in2 = pDataset_in2.GetLayer(0)

    pLayer_out = pDataset_out.CreateLayer('flowline', pSpatialRef_in, ogr.wkbLineString)
    # Add one attribute
    pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn_out = pLayer_out.GetLayerDefn()
    pFeature_out = ogr.Feature(pLayerDefn_out)
    nfeature1 = pLayer_in1.GetFeatureCount()
    nfeature2 = pLayer_in2.GetFeatureCount()
    
    aVertex_head=[]
    aVertex_middle=[]
    aVertex_confluence=[]
    
    
            
    for i in range(0, nfeature1):      
        pFeature_in = pLayer_in1.GetFeature(i)
        pGeometry_in = pFeature_in.GetGeometryRef()
        npoint = pGeometry_in.GetPointCount()        
        pt_start = pGeometry_in.GetPoint(0)
        pt_end = pGeometry_in.GetPoint(npoint-1)

        if pt_start in aVertex_head:
            
            pass
        else:
            if pt_end in aVertex_head:
                pass

    
       


    pFeature_out.SetField("id", lID)
        
    # Add new pFeature_shapefile to output Layer
    pLayer_out.CreateFeature(pFeature_out)        
    pDataset_out.FlushCache()
    
    pDataset_out = pLayer_out = pFeature_out = None    

    return 
