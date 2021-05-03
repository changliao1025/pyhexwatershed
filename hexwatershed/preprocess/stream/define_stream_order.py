import os, sys
import numpy as np 
from osgeo import ogr, osr, gdal, gdalconst
from hexwatershed.preprocess.stream.check_same_point  import check_same_point
def define_stream_order(sFilename_flowline_in, sFilename_flowline_out):
    if  os.path.exists(sFilename_flowline_in)  : 
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
        pLayer_out.CreateField(ogr.FieldDefn('strord', ogr.OFTInteger))
        pLayerDefn_out = pLayer_out.GetLayerDefn()
        pFeature_out = ogr.Feature(pLayerDefn_out)

        nfeature = pLayer_in.GetFeatureCount()

        aStream_order = np.full(nfeature, 0,dtype=int)


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

        for i in range(nfeature):
            pFeature_in = pLayer_in.GetFeature(i)            
            pGeometry_in = pFeature_in.GetGeometryRef()     
            npt = pGeometry_in.GetPointCount()        
            sGeometry_type = pGeometry_in.GetGeometryName()
            if(sGeometry_type == 'LINESTRING'):
                npoint = pGeometry_in.GetPointCount()
                pPoint_start=pGeometry_in.GetPoint(0)

                if (check_head_water(pPoint_start)==1):     
                    aStream_order[i] = 1
        

        #now 
        while aStream_order[0] == 0:

            for  i in range(nfeature):
                if aStream_order[i] !=0:
                    continue

                pFeature_in = pLayer_in.GetFeature(i)            
                pGeometry_in = pFeature_in.GetGeometryRef()     
                npt = pGeometry_in.GetPointCount()        
                sGeometry_type = pGeometry_in.GetGeometryName()
                iFlag_upstream_done = 1
                pPoint_start=pGeometry_in.GetPoint(0)
                pPoint_end=pGeometry_in.GetPoint(npt-1)
                aStrord=list()
                for  j in range(nfeature):
                    pFeature_in2 = pLayer_in.GetFeature(j)            
                    pGeometry_in2 = pFeature_in2.GetGeometryRef()     
                    npoint2 = pGeometry_in2.GetPointCount()  
                    pPoint_start2=pGeometry_in2.GetPoint(0)
                    pPoint_end2=pGeometry_in2.GetPoint(npoint2-1)
                    if (check_same_point(pPoint_start, pPoint_end2)==1):
                        if aStream_order[j] ==0:
                            iFlag_upstream_done=0
                        else:
                            aStrord.append( aStream_order[j]  )
                
                if(iFlag_upstream_done==1):

                    if aStrord[0]==aStrord[1]:
                        aStream_order[i] = aStrord[0] + 1
                    else:
                        aStream_order[i] = np.max(aStrord)


        #save out
        lID =0
        for i in range(0,nfeature ):
            pFeature_in = pLayer_in.GetFeature(i)            
            pGeometry_in = pFeature_in.GetGeometryRef()   
            
            pFeature_out.SetGeometry(pGeometry_in)
            pFeature_out.SetField("id", lID)
            iStream_order= int(aStream_order[i])
           
            pFeature_out.SetField("strord", iStream_order )

            lID = lID + 1    
            pLayer_out.CreateFeature(pFeature_out)        
    
    pDataset_out.FlushCache()

    return