import sys, os
import numpy as np
from osgeo import gdal, osr, ogr, gdalconst

from hexwatershed.preprocess.stream.simplification.add_unique_line import  add_unique_line
from hexwatershed.preprocess.stream.check_same_point  import check_same_point

def remove_small_river(sFilename_flowline_in, sFilename_flowline_out, dThreshold):

    if  os.path.exists(sFilename_flowline_in): 
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

    pDataset_in = pDriver.Open(sFilename_flowline_in, gdal.GA_ReadOnly) 

    # Check to see if shapefile is found.
    if pDataset_in is None:
        print ('Could not open %s' % (sFilename_flowline_in))
    else:
        print ('Opened %s' % (sFilename_flowline_in))
        pLayer_in = pDataset_in.GetLayer()
        pSpatailRef_in = pLayer_in.GetSpatialRef() 

        #output
        pSpatailRef_out = pSpatailRef_in
        pDataset_out = pDriver.CreateDataSource(sFilename_flowline_out)
        pLayer_out = pDataset_out.CreateLayer('flowline', pSpatailRef_out, ogr.wkbLineString)
        # Add one attribute
        pLayer_out.CreateField(ogr.FieldDefn('id', ogr.OFTInteger))
        pLayerDefn = pLayer_out.GetLayerDefn()
        pFeature_out = ogr.Feature(pLayerDefn)
        nfeature = pLayer_in.GetFeatureCount()
        
  
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

        lID=0
        
        for i in range(nfeature):
            pFeature_in = pLayer_in.GetFeature(i)            
            pGeometry_in = pFeature_in.GetGeometryRef()     
            npt = pGeometry_in.GetPointCount()        

            pt_start = pGeometry_in.GetPoint(0)         
            pt_end = pGeometry_in.GetPoint(npt-1)  
            
            dLength = pGeometry_in.Length()
            if check_head_water(pt_start)==1:
                if dLength > dThreshold :
                    pFeature_out.SetGeometry(pGeometry_in)
                    pFeature_out.SetField("id", lID)
                    pLayer_out.CreateFeature(pFeature_out) 
                    lID = lID +1
                else:
                    #print('small')
                    pass
            else:
            
                pFeature_out.SetGeometry(pGeometry_in)
                pFeature_out.SetField("id", lID)
                pLayer_out.CreateFeature(pFeature_out) 
                lID = lID +1

           
                pass

            
            

            pass
     
        pDataset_out = pLayer_out = pFeatureOut  = None      

    return