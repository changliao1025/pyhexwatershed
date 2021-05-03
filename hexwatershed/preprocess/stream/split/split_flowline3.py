import os, sys
from osgeo import ogr, osr, gdal, gdalconst
import numpy as np



def split_flowline3(sFilename_in1, sFilename_in2, sFilename_out):

    if  os.path.exists(sFilename_in1) and os.path.exists(sFilename_in2) : 
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

    #read the vertec dic
    aVertex=[]
    for i in range(0, nfeature2):      
        pFeature_in2 = pLayer_in2.GetFeature(i)
        pGeometry_in2 = pFeature_in2.GetGeometryRef()
        point = pGeometry_in2.GetPoint(0)
        aVertex.append(point)

    for i in range(0, nfeature1):      
        pFeature_in1 = pLayer_in1.GetFeature(i)
        pGeometry_in1 = pFeature_in1.GetGeometryRef()
        npoint = pGeometry_in1.GetPointCount()        

        point_start = pGeometry_in1.GetPoint(0)     
        point_end = pGeometry_in1.GetPoint(npoint-1)
        
        j = 0 
   
       
        iCount =0
        aVertex2=[]
        aVertex3=[]
        for j in range(0,npoint):
            point = pGeometry_in1.GetPoint(j)
            #use a more precise method here
            if point in aVertex: 
                iCount = iCount +1
                aVertex2.append(j)
                aVertex3.append(point)
            else:
                pass

        if  iCount ==2:
            #this is single 
            pFeature_out.SetGeometry(pGeometry_in1)
            pFeature_out.SetField("id", lID)
            lID = lID + 1        
            # Add new pFeature_shapefile to output Layer
            pLayer_out.CreateFeature(pFeature_out)        

        else:
            nLine = iCount-1
            for k in range(nLine):

                ii = aVertex2[k]
                jj= aVertex2[k+1]
                line = ogr.Geometry(ogr.wkbLineString)
                for kk in range(ii,jj+1):                    
                    pointkk= pGeometry_in1.GetPoint(kk)
                    line.AddPoint(pointkk[0], pointkk[1])
                    pass
                pFeature_out.SetGeometry(line)
                pFeature_out.SetField("id", lID)
                lID = lID + 1        
            
                pLayer_out.CreateFeature(pFeature_out)   
                pass


            pass


    pDataset_out.FlushCache()
    pDataset_out = pLayer_out = pFeature_out = None    

    return 