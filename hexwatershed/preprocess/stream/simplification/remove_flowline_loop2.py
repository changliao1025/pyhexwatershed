import sys, os
import numpy as np
from osgeo import gdal, osr, ogr, gdalconst
from itertools import combinations

from hexwatershed.preprocess.stream.add_unique_point import  add_unique_point

def remove_flowline_loop2(sFilename_flowline_in, sFilename_confluence_in, sFilename_flowline_out):
    if  os.path.exists(sFilename_flowline_in) and os.path.exists(sFilename_confluence_in): 
        pass
    else:
        print('The input file does not exist')
        return

    if os.path.exists(sFilename_flowline_out): 
        #delete it if it exists
        os.remove(sFilename_flowline_out)

    sDriverName = "GeoJSON"
    pDriver = ogr.GetDriverByName( sDriverName )

    if pDriver is None:
        print ("%s pDriver not available.\n" % sDriverName)
    else:
        print  ("%s pDriver IS available.\n" % sDriverName)

    pDataset_in1 = pDriver.Open(sFilename_flowline_in, gdal.GA_ReadOnly) 

  
    if pDataset_in1 is None:
        print ('Could not open %s' % (sFilename_flowline_in))
    else:
        print ('Opened %s' % (sFilename_flowline_in))
        pLayer_in1 = pDataset_in1.GetLayer()
        pSpatailRef_in = pLayer_in1.GetSpatialRef() 

        #output
        pSpatailRef_out = pSpatailRef_in
        pDataset_out = pDriver.CreateDataSource(sFilename_flowline_out)
        pLayer_out = pDataset_out.CreateLayer('flowline', pSpatailRef_out, ogr.wkbLineString)
        # Add one attribute
        pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        pLayerDefn = pLayer_out.GetLayerDefn()
        pFeatureOut = ogr.Feature(pLayerDefn)
        nfeature1 = pLayer_in1.GetFeatureCount()
        print ( "Number of features in %s: %d" %  (os.path.basename(sFilename_flowline_in),nfeature1) )    
        
        lID = 0
        
        aFlowline = combinations(range(nfeature1), 3) 
        aFlag_done = np.full(nfeature1, 0,dtype=int)
        aFlag_removed = np.full(nfeature1, 0,dtype=int)
        for gFlowline in aFlowline:            
            abc = aFlag_removed[gFlowline[0]] +  aFlag_removed[gFlowline[1]]\
                 + aFlag_removed[gFlowline[2]] 
            if(  abc !=0 ):
                continue

            pFeature_in1 = pLayer_in1.GetFeature(gFlowline[0])
            pFeature_in2 = pLayer_in1.GetFeature(gFlowline[1])
            pFeature_in3 = pLayer_in1.GetFeature(gFlowline[2])
            
            pGeometry_in1 = pFeature_in1.GetGeometryRef()     
            pGeometry_in2 = pFeature_in2.GetGeometryRef()   
            pGeometry_in3 = pFeature_in3.GetGeometryRef()   
            npt1 = pGeometry_in1.GetPointCount()         
            npt2 = pGeometry_in2.GetPointCount()         
            npt3 = pGeometry_in3.GetPointCount()         
            aPt_pair1 = [ pGeometry_in1.GetPoint(0), pGeometry_in1.GetPoint(npt1-1)]
            aPt_pair2 = [ pGeometry_in2.GetPoint(0), pGeometry_in2.GetPoint(npt2-1)]
            aPt_pair3 = [ pGeometry_in3.GetPoint(0), pGeometry_in3.GetPoint(npt3-1)]

            aPoint =[]
            iFlag= 0

            iFlag, aPoint = add_unique_point(aPoint, aPt_pair1[0])
            iFlag, aPoint = add_unique_point(aPoint, aPt_pair1[1])
            iFlag, aPoint = add_unique_point(aPoint, aPt_pair2[0])
            iFlag, aPoint = add_unique_point(aPoint, aPt_pair2[1])
            iFlag, aPoint = add_unique_point(aPoint, aPt_pair3[0])
            iFlag, aPoint = add_unique_point(aPoint, aPt_pair3[1])

            npt0 = len(aPoint)
            if (npt0==3):
                #we need to remove one of them                               
                aFlag_removed[gFlowline[1]] = 1                
                aFlag_removed[gFlowline[2]] = 1

                pass
            else:                     
                pass
                

            pass
    
        lID=0
        for i in range( nfeature1 ):
            pFeature_in1 = pLayer_in1.GetFeature(i)
            pGeometry_in1 = pFeature_in1.GetGeometryRef()
            if(aFlag_removed[i] != 1):

                pFeatureOut.SetGeometry(pGeometry_in1)
                pFeatureOut.SetField("id", lID)
                pLayer_out.CreateFeature(pFeatureOut)
                lID=lID+1

     
        pDataset_out = pLayer_out = pFeatureOut  = None      

    return