import os, sys
import numpy as np
from osgeo import ogr, osr, gdal, gdalconst
from shapely.geometry import Point, LineString
from shapely.ops import split
from shapely.wkt import loads

def split_flowline2(sFilename_in, sFilename_in2, sFilename_out):
    if  os.path.exists(sFilename_in) and os.path.exists(sFilename_in2): 
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
    pLayer_in1 = pDataset_in.GetLayer(0)
    pSpatialRef_in = pLayer_in1.GetSpatialRef()
    nfeature1 = pLayer_in1.GetFeatureCount()


    pDataset_in2 = pDriver.Open(sFilename_in2, gdal.GA_ReadOnly)
    pLayer_in2 = pDataset_in2.GetLayer(0)
    nfeature2 = pLayer_in2.GetFeatureCount()
    

    pLayer_out = pDataset_out.CreateLayer('flowline', pSpatialRef_in, ogr.wkbLineString)
    # Add one attribute
    pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger64)) #long type for high resolution
    
    pLayerDefn_out = pLayer_out.GetLayerDefn()
    pFeature_out = ogr.Feature(pLayerDefn_out)
    
    lID =0
    for i in range(0, nfeature1):  
        pFeature_in1 = pLayer_in1.GetFeature(i)
        pGeometry_in1 = pFeature_in1.GetGeometryRef()        

        sGeometry_type = pGeometry_in1.GetGeometryName()
        if(sGeometry_type == 'MULTILINESTRING'):
            #this should not happend
            pass
        else:
            if sGeometry_type =='LINESTRING':

                line = loads( pGeometry_in1.ExportToWkt() )
                for j in range(0, nfeature2):  
                    pFeature_in2 = pLayer_in2.GetFeature(j)
                    pGeometry_in2 = pFeature_in2.GetGeometryRef()
                    pt = loads( pGeometry_in2.ExportToWkt() )
                    coords = line.coords
                    npoint = len(coords)
                    if npoint <=3:
                        if npoint ==2:
                            iFlag_single=1
                            break                            
                        else:
                            pt0 = Point(coords[1] )
                            if pt0.distance(pt)< 1e-8:
                                #same point
                                #print('wow')
                                for k in range(2):
                                    line3= LineString( coords[k: k+2] )
                                    pGeometry_out = ogr.CreateGeometryFromWkb(line3.wkb)
                                    pFeature_out.SetGeometry(pGeometry_out)
                                    pFeature_out.SetField("id", lID)
                                    lID = lID + 1                                
                                    pLayer_out.CreateFeature(pFeature_out)   
                                pass
                            else:
                                pass
                    else:

                        line2 = LineString( coords[1: npoint-1] )
                        dd = line2.distance(pt)
                        if dd < 1e-8 :
                            iFlag_single = 0
                            aGeometry = split(line, pt)
                            nline = len(aGeometry)                       
                            if nline == 2:
                                for pGeometry in aGeometry:
                                    pGeometry_out = ogr.CreateGeometryFromWkb(pGeometry.wkb)
                                    pFeature_out.SetGeometry(pGeometry_out)
                                    pFeature_out.SetField("id", lID)
                                    lID = lID + 1                                
                                    pLayer_out.CreateFeature(pFeature_out)    
                            else:
                                print('no intersection')
                                pass
                            break
                        else:
                            iFlag_single =1

                if  iFlag_single ==1:
                    pFeature_out.SetGeometry(pGeometry_in1)
                    pFeature_out.SetField("id", lID)
                    lID = lID + 1                    
                    pLayer_out.CreateFeature(pFeature_out)  

            else:
                print(sGeometry_type)
                pass
            
    
    pDataset_out.FlushCache()
    pDataset_out = pLayer_out = pFeature_out = None    

    return 