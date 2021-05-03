import os, sys
from osgeo import ogr, osr, gdal, gdalconst
import numpy as np

#from hexwatershed.preprocess.stream.add_unique_point import add_unique_point
from hexwatershed.preprocess.stream.check_same_point  import check_same_point
from hexwatershed.preprocess.stream.find_vertex_in_list  import find_vertex_in_list

def find_flowline_vertex2(sFilename_in, sFilename_out):
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
    pLayer_out.CreateField(ogr.FieldDefn('isconf', ogr.OFTInteger)) #long type for high resolution
    
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
            if find_vertex_in_list(aVertex,pPoint_start )!=-1:                
                pass
            else:
                aVertex.append(pPoint_start)
            if find_vertex_in_list(aVertex,pPoint_end )!=-1:                
                pass
            else:
                aVertex.append(pPoint_end)

        else:
            print('You need to split line before using this function!')
            return

    def check_head_water(pt): #need to remove the outlet because it is not a headwater
        iFlag= 0
        iCount=0
        for i in range(0, nfeature):
            pFeature_in2 = pLayer_in.GetFeature(i)
            
            pGeometry_in2 = pFeature_in2.GetGeometryRef()
            npt2 = pGeometry_in2.GetPointCount()
            pt1 = pGeometry_in2.GetPoint(0)
            pt2 = pGeometry_in2.GetPoint(npt2-1)
            if (check_same_point(pt, pt1)==1):
                iCount = iCount +1
            else:
                pass

            if (check_same_point(pt, pt2)==1):
                iCount = iCount +1
                
            else:
                pass

        if (iCount ==1):
            iFlag=1
        else:
            iFlag=0

        return iFlag

    #calculate confluence
    nvertex = len(aVertex)
    aConfluence = np.full(nvertex, 0,dtype=int)
    aFlag_confluence = np.full(nvertex, 0,dtype=int)
    for i in range(0, nfeature):      
        pFeature_in = pLayer_in.GetFeature(i)
        pGeometry_in = pFeature_in.GetGeometryRef()
        sGeometry_type = pGeometry_in.GetGeometryName()
        if(sGeometry_type == 'LINESTRING'):
            npoint = pGeometry_in.GetPointCount()
            pPoint_start=pGeometry_in.GetPoint(0)
            pPoint_end=pGeometry_in.GetPoint(npoint-1)        
            j = find_vertex_in_list(aVertex, pPoint_start)#aVertex.index(pPoint_start) 
            k = find_vertex_in_list(aVertex, pPoint_end)#aVertex.index(pPoint_end)        
            
            if i == 0:    
                aConfluence[j]=aConfluence[j]+1
                aConfluence[k] = 0 #use 0 to mark outlet
                pass
            else:

                if (check_head_water(pPoint_start)==1):     
                    
                    aConfluence[j] = 1

                else:
                    aConfluence[j]=aConfluence[j]+1
                
                
                               
                aConfluence[k] = aConfluence[k]  +1
            

            
        else:
            
            return

    for i in range(0, nvertex): 
        if (aConfluence[i] >=3):
            aFlag_confluence[i] = 1
        else:
            if (aConfluence[i] ==1):
                aFlag_confluence[i] = 0
            else:
                aFlag_confluence[i] = 0

    lID = 0
    for i in range(0,nvertex ):
        pPoint = aVertex[i]
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(pPoint[0], pPoint[1])
        pFeature_out.SetGeometry(point)
        pFeature_out.SetField("id", lID)
        iflag = int(aConfluence[i])
        pFeature_out.SetField("isconf", iflag )
        
        lID = lID + 1    
        pLayer_out.CreateFeature(pFeature_out)        
    
    pDataset_out.FlushCache()
    pDataset_out = pLayer_out = pFeature_out = None    
    return
