import os, sys
from osgeo import ogr, osr, gdal, gdalconst
import numpy as np

from hexwatershed.preprocess.stream.add_unique_point import add_unique_point

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

    
    
    aVertex = []
    #print( type(aVertex))
    nfeature = pLayer_in.GetFeatureCount()
    #build dictionary
    for i in range(0, nfeature):      
        pFeature_in = pLayer_in.GetFeature(i)
        pGeometry_in = pFeature_in.GetGeometryRef()
        sGeometry_type = pGeometry_in.GetGeometryName()
        if(sGeometry_type == 'LINESTRING'):
            npoint = pGeometry_in.GetPointCount()
            pPoint_start=pGeometry_in.GetPoint(0)
            pPoint_end=pGeometry_in.GetPoint(npoint-1)        
            if pPoint_start in aVertex:                
                pass
            else:
                aVertex.append(pPoint_start)
            if pPoint_end in aVertex:                
                pass
            else:
                aVertex.append(pPoint_end)

                #iFlag, aPoint = add_unique_point(aVertex, pPoint_start)
                #iFlag, aPoint = add_unique_point(aVertex, pPoint_end)
        else:
            print('You need to split line before using this function!')
            return
    #calculate confluence
    nvertex = len(aVertex)
    
  

    lID = 0
    for i in range(0,nvertex ):
        pPoint = aVertex[i]
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(pPoint[0], pPoint[1])
        pFeature_out.SetGeometry(point)
        pFeature_out.SetField("id", lID)
        #iflag = int(aFlag_confluence[i])
        #pFeature_out.SetField("isconf", iflag )
        
        lID = lID + 1    
        pLayer_out.CreateFeature(pFeature_out)        
    
    pDataset_out.FlushCache()
    pDataset_out = pLayer_out = pFeature_out = None    
    return
