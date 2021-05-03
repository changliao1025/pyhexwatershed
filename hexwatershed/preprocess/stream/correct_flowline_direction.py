import os, sys
import numpy as np 
from osgeo import ogr, osr, gdal, gdalconst
from shapely.geometry import Point, LineString
from shapely.ops import split
from shapely.wkt import loads
from hexwatershed.preprocess.stream.check_same_point  import check_same_point

lID=0
aFlag_process=None
def correct_flowline_direction(sFilename_in, sFilename_out):
    if  os.path.exists(sFilename_in): 
        pass
    else: 
        print('The input file does not exist')
        return
        
    if os.path.exists(sFilename_out): 
        #delete it if it exists
        os.remove(sFilename_out)

    pDriver = ogr.GetDriverByName('GeoJSON')
    pDriver2 = ogr.GetDriverByName('ESRI Shapefile')
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
    lOutlet = 1

    #we have to go reversely
    iFeature_current= lOutlet

    pFeature_in = pLayer_in.GetFeature(iFeature_current)

    pGeometry_in = pFeature_in.GetGeometryRef()
    npt = pGeometry_in.GetPointCount()
    pt_start = pGeometry_in.GetPoint(0)
    pt_end = pGeometry_in.GetPoint(npt-1)

    global lID
    pFeature_out.SetGeometry(pGeometry_in)
    pFeature_out.SetField("id", lID)
        
    # Add new pFeature_shapefile to output Layer
    pLayer_out.CreateFeature(pFeature_out)    

    def check_head_water(pt):
        iFlag= -1
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
                pass

        if iCount ==1:
            iFlag=1

        return iFlag

    #we might find more than 1 upstream
    global aFlag_process
    aFlag_process=np.full(nfeature, 0, dtype =int)
    def find_upstream_flowline(pt_start_in, pt_end_in):

        nupstream=0
        aUpstream=[]
        aFlag_reverse=[]
        global aFlag_process

       
        for i in range(0, nfeature):
            pFeature_in2 = pLayer_in.GetFeature(i)
            pGeometry_in2 = pFeature_in2.GetGeometryRef()
            npt2 = pGeometry_in2.GetPointCount()
            pt1 = pGeometry_in2.GetPoint(0)
            pt2 = pGeometry_in2.GetPoint(npt2-1)
            if (check_same_point(pt_start_in, pt1)==1  and check_same_point(pt_end_in, pt2)!=1):
                #this one should be reversed
                if aFlag_process[i] !=1:
                    aUpstream.append(i )
                    aFlag_reverse.append(1)
                    aFlag_process[i] =1
            else:
                if (check_same_point(pt_start_in, pt2)==1 ):
                    #this is the one we are
                    if aFlag_process[i] !=1:
                        aUpstream.append(i )
                        aFlag_reverse.append(0)
                        aFlag_process[i] =1
                    
                else:
                    
                    pass
        nupstream = len(aUpstream)
        return nupstream, aUpstream, aFlag_reverse
    
    lID= lID+1
    def tag_upstream(pt_start, pt_end):
        if(check_head_water(pt_start)!=1):
            #print(pt_start, pt_end)
            #find the next flowline get to this 
            nUp, aUp, aReverse = find_upstream_flowline(pt_start, pt_end)
            if nUp > 0:
                global lID
                #if nUp==2:
                    #print('care')
                for j in range(nUp):
                    if (aReverse[j]==1):
                        pFeature_in2 = pLayer_in.GetFeature(  aUp[j] )

                        pGeometry_in2 = pFeature_in2.GetGeometryRef()
                        npt2 = pGeometry_in2.GetPointCount()

                        line = loads( pGeometry_in2.ExportToWkt() )
                        coords = line.coords
                        line2= LineString( coords[::-1 ] )

                        pGeometry_out = ogr.CreateGeometryFromWkb(line2.wkb)

                        pFeature_out.SetGeometry(pGeometry_out)
                        pFeature_out.SetField("id", lID)
                        pLayer_out.CreateFeature(pFeature_out) 
                        lID = lID +1

                        #pt_start = pGeometry_in2.GetPoint(0)
                        pt_start = pGeometry_in2.GetPoint(npt2-1)
                        pt_end = pGeometry_in2.GetPoint(0)
                    
                        tag_upstream(pt_start, pt_end)
                        
                    else:
                        pFeature_in2 = pLayer_in.GetFeature(  aUp[j] )

                        pGeometry_in2 = pFeature_in2.GetGeometryRef()
                        npt2 = pGeometry_in2.GetPointCount()

                        pFeature_out.SetGeometry(pGeometry_in2)
                        pFeature_out.SetField("id", lID)
                        pLayer_out.CreateFeature(pFeature_out) 
                        lID = lID +1
                        pt_start = pGeometry_in2.GetPoint(0)
                        pt_end = pGeometry_in2.GetPoint(npt2-1)
                        tag_upstream(pt_start, pt_end)
                pass
            else:
                pass

    tag_upstream(pt_start, pt_end)
    pDataset_out.FlushCache()
    
    pDataset_out = pLayer_out = pFeature_out = None    
    return