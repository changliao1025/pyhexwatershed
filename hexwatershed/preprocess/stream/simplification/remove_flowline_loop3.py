import sys, os
import numpy as np
from osgeo import gdal, osr, ogr, gdalconst

from hexwatershed.preprocess.stream.simplification.add_unique_line import  add_unique_line
from hexwatershed.preprocess.stream.check_same_point  import check_same_point

def remove_flowline_loop3(sFilename_flowline_in, sFilename_flowline_out):

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
        pFeatureOut = ogr.Feature(pLayerDefn)
        nfeature = pLayer_in.GetFeatureCount()
        
        
        j = 0
        aLine =[]

        def find_paralle_stream(i, pt_start):
            iFlag =0
            ndownstream=0
            aDownstream=[]
            for j in range(nfeature):
                pFeature_in = pLayer_in.GetFeature(j)            
                pGeometry_in = pFeature_in.GetGeometryRef()     
                npt = pGeometry_in.GetPointCount()            
                pt1_start = pGeometry_in.GetPoint(0)         
                pt1_end = pGeometry_in.GetPoint(npt-1)  
                if check_same_point(pt_start, pt1_start)==1 and j !=i :
                    ndownstream= ndownstream+1
                    aDownstream.append(j)
                    


            return ndownstream, aDownstream

        lID=0
        aFlag = np.full(nfeature, 0, dtype=int)
        for i in range(nfeature):
            pFeature_in = pLayer_in.GetFeature(i)            
            pGeometry_in = pFeature_in.GetGeometryRef()     
            npt = pGeometry_in.GetPointCount()        

            pt_start = pGeometry_in.GetPoint(0)         
            pt_end = pGeometry_in.GetPoint(npt-1)  
            ndownstream , aDownstream = find_paralle_stream(i, pt_start)
            if ndownstream == 0:
                if aFlag[i] !=1:
                    pFeatureOut.SetGeometry(pGeometry_in)
                    pFeatureOut.SetField("id", lID)
                    pLayer_out.CreateFeature(pFeatureOut)
                    lID = lID + 1
                    aFlag[i]=1
                pass
            else:                     
                #more than one, so we only take one
                if(ndownstream>0):
                    
                    if aFlag[i] !=1:
                        pFeatureOut.SetGeometry(pGeometry_in)
                        pFeatureOut.SetField("id", lID)
                        pLayer_out.CreateFeature(pFeatureOut)
                        lID = lID + 1
                        aFlag[i]=1

                    for k in range(ndownstream):

                        aFlag[  aDownstream[k]] =1

                pass
            

            pass
     
        pDataset_out = pLayer_out = pFeatureOut  = None      

    return